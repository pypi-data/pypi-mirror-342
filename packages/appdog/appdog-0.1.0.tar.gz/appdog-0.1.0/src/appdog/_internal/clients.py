import json
import typing
from pathlib import Path
from typing import Any, TypeVar

import httpx
from httpx import AsyncClient, Timeout
from pydantic import TypeAdapter
from typing_extensions import Self, TypedDict, Unpack

from .errors import (
    AuthError,
    NotFoundError,
    RateLimitError,
    RequestError,
    ResponseError,
)
from .project import Project
from .settings import ClientSettings
from .typing import Undefined, UndefinedType

_T = TypeVar('_T')


class ClientConfig(TypedDict, total=False):
    """Client arguments."""

    base_url: str | None
    """Base URL for the client."""

    api_key: str | None
    """API key for authentication."""

    token: str | None
    """Bearer token for authentication."""

    api_key_header: str | None
    """Header name for API key."""

    token_header: str | None
    """Header name for bearer token."""

    timeout: float | None
    """Request timeout in seconds."""

    strict: bool | None
    """Whether to raise an error for invalid response data."""


class BaseClient:
    """Base client for API services."""

    paths: dict[str, str] = {}
    """Paths for the client."""

    def __init__(self, name: str, **config: Unpack[ClientConfig]) -> None:
        base_url = config.pop('base_url', None)
        if not base_url:
            raise ValueError('A base URL is required')
        self._client: AsyncClient | None = None
        self._settings = ClientSettings.with_env_prefix(name=name, base_url=base_url, **config)

    async def __aenter__(self) -> Self:
        self.open()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    @classmethod
    def load(cls, name: str, project_dir: Path | str | None = None) -> Self:
        """Load the client from the project directory."""
        project = Project.load(project_dir)
        if name not in project.settings:
            return cls(name)
        config = project.settings[name].get_client_config()
        return cls(name, **config)

    def open(self) -> None:
        """Open the HTTP client."""
        if self._client is None:
            self._client = self._create_client()

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _create_client(self) -> AsyncClient:
        """Create a new HTTP client."""
        return AsyncClient(
            base_url=self._settings.base_url,
            headers=self._settings.get_headers(),
            timeout=self._settings.timeout,
        )

    @typing.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _request(  # noqa: C901
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make an API request.

        Args:
            method: HTTP method
            path: URL path
            params: Query parameters
            data: Request body data
            headers: Additional headers
            return_type: Type or Pydantic type adapter to convert the response data

        Returns:
            API response data, optionally converted with the provided type

        Raises:
            ClientError: If the request fails.
        """
        client = self._client
        close_on_exit = False
        if client is None:
            client = self._create_client()
            close_on_exit = True

        timeout = Timeout(self._settings.timeout, connect=5.0)

        if not path.startswith('/'):
            path = f'/{path}'
        headers = headers or {}
        headers = {**self._settings.get_headers(), **headers}
        if data is not None and hasattr(data, 'model_dump') and callable(data.model_dump):
            data = data.model_dump(mode='json')

        try:
            response = await client.request(
                method=method,
                url=path,
                params=params,
                json=data,
                headers=headers,
                timeout=timeout,
            )

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                error_detail = str(e)
                try:
                    error_json = response.json()
                    if isinstance(error_json, dict) and 'message' in error_json:
                        error_detail = error_json['message']
                except json.JSONDecodeError:
                    pass

                if response.status_code in (401, 403):
                    raise AuthError(
                        f'Authentication error: {error_detail}',
                        status_code=response.status_code,
                        response=response,
                    ) from e
                elif response.status_code == 404:
                    raise NotFoundError(
                        f'Resource not found: {error_detail}',
                        status_code=response.status_code,
                        response=response,
                    ) from e
                elif response.status_code == 429:
                    raise RateLimitError(
                        f'Rate limit exceeded: {error_detail}',
                        status_code=response.status_code,
                        response=response,
                    ) from e
                elif 400 <= response.status_code < 500:
                    raise ResponseError(
                        f'Client error: {error_detail}',
                        status_code=response.status_code,
                        response=response,
                    ) from e
                else:
                    raise ResponseError(
                        f'Server error: {error_detail}',
                        status_code=response.status_code,
                        response=response,
                    ) from e

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text

            if return_type is Undefined:
                return response_data

            try:
                if not isinstance(return_type, TypeAdapter):
                    return_type = TypeAdapter(return_type)
                return return_type.validate_python(response_data)
            except Exception as e:
                if not self._settings.strict:
                    return response_data
                raise ResponseError(
                    f'Validation error: {e}',
                    status_code=response.status_code,
                    response=response,
                ) from e

        except httpx.RequestError as e:
            raise RequestError('Request failed') from e
        finally:
            if close_on_exit:
                await client.aclose()

    @typing.overload
    async def _get(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _get(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _get(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make a GET request."""
        return await self._request(
            'GET',
            path,
            data=data,
            params=params,
            headers=headers,
            return_type=return_type,
        )

    @typing.overload
    async def _post(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _post(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _post(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make a POST request."""
        return await self._request(
            'POST',
            path,
            params=params,
            data=data,
            headers=headers,
            return_type=return_type,
        )

    @typing.overload
    async def _put(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _put(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _put(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make a PUT request."""
        return await self._request(
            'PUT',
            path,
            params=params,
            data=data,
            headers=headers,
            return_type=return_type,
        )

    @typing.overload
    async def _patch(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _patch(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _patch(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make a PATCH request."""
        return await self._request(
            'PATCH',
            path,
            params=params,
            data=data,
            headers=headers,
            return_type=return_type,
        )

    @typing.overload
    async def _delete(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: UndefinedType = Undefined,
    ) -> Any: ...

    @typing.overload
    async def _delete(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T],
    ) -> _T: ...

    async def _delete(
        self,
        path: str,
        *,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_type: TypeAdapter[_T] | type[_T] | UndefinedType = Undefined,
    ) -> Any | _T:
        """Make a DELETE request."""
        return await self._request(
            'DELETE',
            path,
            data=data,
            params=params,
            headers=headers,
            return_type=return_type,
        )
