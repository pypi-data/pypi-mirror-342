import dataclasses
import datetime
import json
import os
import re
from re import Pattern
from typing import Any

import httpx
from pydantic import BaseModel
from typing_extensions import Self, TypedDict, Unpack

from .case import to_name_case
from .logging import logger
from .utils import compute_hash


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class EndpointInfo:
    """An API endpoint information."""

    name: str
    """Generated endpoint function name."""

    method: str
    """HTTP method."""

    path: str
    """URL path."""

    tags: list[str]
    """Tags."""

    operation_id: str
    """Operation identifier."""

    summary: str
    """Summary."""

    description: str
    """Description."""

    parameters: list[dict[str, Any]]
    """List of parameters."""

    request_body: dict[str, Any] | None
    """Request body schema."""

    responses: dict[str, dict[str, Any]]
    """Response schemas."""


class LookupConfig(TypedDict, total=False):
    """A configuration dictionary for endpoint lookup."""

    include_methods: list[str] | None
    """List of HTTP methods to include."""

    exclude_methods: list[str] | None
    """List of HTTP methods to exclude."""

    include_tags: list[str] | None
    """List of tags to include."""

    exclude_tags: list[str] | None
    """List of tags to exclude."""

    filters: dict[str, Pattern | str] | None
    """Filters to apply to endpoints information."""


class AppSpec(BaseModel, frozen=True):
    """Application OpenAPI specification."""

    uri: str
    """URI to OpenAPI specification."""

    data: dict[str, Any]
    """OpenAPI specification data."""

    timestamp: datetime.datetime
    """Timestamp of the last refresh."""

    hash: str
    """OpenAPI specification hash."""

    @classmethod
    async def fetch(cls, uri: str) -> Self:
        """Fetch the application OpenAPI specification from the given URI."""
        logger.info(f'Fetching application specification from {uri}')
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        # Handle local resources
        if os.path.exists(uri):
            try:
                with open(uri) as f:
                    data = dict(json.load(f))
            except Exception as e:
                raise ValueError(f'Failed to parse local specification from {uri!r}') from e

        # Handle remote resources
        elif uri.startswith('http://') or uri.startswith('https://'):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(uri)
                    response.raise_for_status()
                    data = dict(response.json())
            except Exception as e:
                raise ValueError(f'Failed to load specification from {uri!r}') from e

        # Handle invalid resources
        else:
            raise ValueError(f'Specification not found for {uri!r}')

        return cls(uri=uri, data=data, hash=compute_hash(data), timestamp=timestamp)

    def lookup(self, **config: Unpack[LookupConfig]) -> list[EndpointInfo]:  # noqa: C901
        """Lookup endpoints with the given filters.

        Args:
            include_methods: List of HTTP methods to include (e.g., [`'get'`, `'post'`])
            exclude_methods: List of HTTP methods to exclude
            include_tags: List of tags to include
            exclude_tags: List of tags to exclude
            filters: Additional filters to apply to endpoints. If a value is a regex Pattern or a
                string, it will be used as a regex pattern to match against the attribute.
                Otherwise, it will check for equality.

        Returns:
            List of filtered endpoint information.

        Example:
            >>> spec.lookup(
            ...     include_methods=['get', 'post'],
            ...     include_tags=['public'],
            ...     path=r'/api/v1/.*'
            ... )
        """

        endpoints: dict[str, EndpointInfo] = {}

        paths = self.data.get('paths', {})
        include_methods = config.get('include_methods')
        exclude_methods = config.get('exclude_methods')
        include_tags = config.get('include_tags')
        exclude_tags = config.get('exclude_tags')
        filters = config.get('filters') or {}

        for path, path_item in paths.items():
            for method, operation in path_item.items():
                # Skip non-HTTP methods and metadata fields
                if method not in ('get', 'post', 'put', 'delete', 'patch'):
                    continue
                # Skip empty operations
                if not operation or not isinstance(operation, dict):
                    continue
                # Apply method filters
                if include_methods and method not in include_methods:
                    continue
                if exclude_methods and method in exclude_methods:
                    continue
                # Apply tag filters
                tags = operation.get('tags', [])
                if include_tags and not any(tag in include_tags for tag in tags):
                    continue
                if exclude_tags and any(tag in exclude_tags for tag in tags):
                    continue
                # Create endpoint info
                name = method.lower() + '_' + to_name_case(path)
                assert name not in endpoints, f'Duplicate endpoint: {name}'
                endpoint = EndpointInfo(
                    name=name,
                    method=method,
                    path=path,
                    tags=tags,
                    operation_id=operation.get('operationId'),
                    summary=operation.get('summary', ''),
                    description=operation.get('description', ''),
                    parameters=operation.get('parameters', []),
                    request_body=operation.get('requestBody'),
                    responses=operation.get('responses', {}),
                )
                # Apply additional filters
                should_include = True
                for attr_name, attr_filter in filters.items():
                    if hasattr(endpoint, attr_name):
                        attr_value = getattr(endpoint, attr_name)
                        if isinstance(attr_filter, Pattern):
                            if not attr_filter.search(str(attr_value)):
                                should_include = False
                                break
                        elif isinstance(attr_filter, str):
                            pattern = re.compile(attr_filter)
                            if not pattern.search(str(attr_value)):
                                should_include = False
                                break
                        elif attr_value != attr_filter:
                            should_include = False
                            break
                if should_include:
                    endpoints[name] = endpoint

        return list(endpoints.values())

    def __eq__(self, other: object) -> bool:
        """Check if two specifications are equal."""
        return self.uri == getattr(other, 'uri', None) and self.hash == getattr(other, 'hash', None)

    def __ne__(self, other: object) -> bool:
        """Check if two specifications are not equal."""
        return not self == other
