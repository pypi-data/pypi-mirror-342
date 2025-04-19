import functools
import typing
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from .case import to_pascal_case, to_snake_case

if typing.TYPE_CHECKING:
    from .clients import ClientConfig
    from .specs import LookupConfig


class AppSettings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(extra='allow')

    uri: str = Field(..., frozen=True)
    """URI to OpenAPI specification."""

    base_url: str | None = None
    """Base URL for API."""

    include_methods: list[str] | None = None
    """Methods to include in mounted endpoints."""

    exclude_methods: list[str] | None = None
    """Methods to exclude from mounted endpoints."""

    include_tags: list[str] | None = None
    """Tags to include in mounted endpoints."""

    exclude_tags: list[str] | None = None
    """Tags to exclude from mounted endpoints."""

    filters: dict[str, str] | None = None
    """Filters to apply to mounted endpoints."""

    timeout: float | None = None
    """Request timeout in seconds."""

    strict: bool | None = None
    """Whether to raise an error for invalid response data."""

    @model_validator(mode='after')
    def model_validate_base_url(self) -> Self:
        if not self.base_url:
            self.base_url = self.uri.rpartition('/')[0]
        return self

    def get_client_config(self) -> 'ClientConfig':
        """Get client configuration."""
        return self.model_dump(  # type: ignore
            include={
                'base_url',
                'api_key',
                'token',
                'api_key_header',
                'token_header',
                'timeout',
                'strict',
            },
        )

    def get_lookup_config(self) -> 'LookupConfig':
        """Get endpoint lookup configuration."""
        return self.model_dump(  # type: ignore
            include={
                'include_methods',
                'exclude_methods',
                'include_tags',
                'exclude_tags',
                'filters',
            },
        )


class ClientSettings(BaseSettings):
    """Client settings."""

    model_config = SettingsConfigDict(extra='allow')

    name: str = Field(..., frozen=True)
    """Application name."""

    base_url: str
    """Base URL for API."""

    api_key: str | None = None
    """API key for authentication."""

    token: str | None = None
    """Bearer token for authentication."""

    api_key_header: str = 'X-API-Key'
    """Header name for API key."""

    token_header: str = 'Authorization'  # noqa: S105
    """Header name for bearer token."""

    timeout: float | None = 30
    """Request timeout in seconds."""

    strict: bool | None = False
    """Whether to raise an error for invalid response data."""

    @classmethod
    def with_env_prefix(cls, **data: Any) -> Self:
        """Create a new instance with client-specific environment variable prefix."""
        # Create a new settings instance that loads values from environment variables with the
        # application prefix "APPDOG_{APP_NAME}_" to allow for client-specific configuration.
        assert 'name' in data, 'Client name is required'
        env_prefix = f'APPDOG_{to_snake_case(data["name"]).upper()}_'
        cls = type(
            f'{to_pascal_case(data["name"])}Settings',
            (cls,),
            {'model_config': SettingsConfigDict(env_prefix=env_prefix, extra='allow')},
        )
        return cls(**data)

    def get_headers(self) -> dict[str, str]:
        """Get headers for client requests."""
        return _compute_headers(self.api_key, self.token, self.api_key_header, self.token_header)


@functools.lru_cache(maxsize=1)
def _compute_headers(
    api_key: str | None,
    token: str | None,
    api_key_header: str,
    token_header: str,
) -> dict[str, str]:
    """Compute headers with caching based on auth credentials."""
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    if api_key:
        headers[api_key_header] = api_key
    if token:
        headers[token_header] = f'Bearer {token}'
    return headers
