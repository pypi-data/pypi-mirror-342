import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from appdog._internal.settings import AppSettings, ClientSettings, _compute_headers


class TestAppSettings:
    """Tests for AppSettings class."""

    def test_init_with_required_fields(self) -> None:
        """Test initialization with required fields."""
        settings = AppSettings(uri='http://example.com/api')
        assert settings.uri == 'http://example.com/api'
        assert settings.base_url == 'http://example.com'
        assert settings.include_methods is None
        assert settings.exclude_methods is None
        assert settings.include_tags is None
        assert settings.exclude_tags is None

    def test_init_with_optional_fields(self) -> None:
        """Test initialization with optional fields."""
        settings = AppSettings(
            uri='http://example.com/api',
            base_url='http://api.example.com',
            include_methods=['GET', 'POST'],
            exclude_methods=['DELETE'],
            include_tags=['public'],
            exclude_tags=['private'],
        )
        assert settings.uri == 'http://example.com/api'
        assert settings.base_url == 'http://api.example.com'
        assert settings.include_methods == ['GET', 'POST']
        assert settings.exclude_methods == ['DELETE']
        assert settings.include_tags == ['public']
        assert settings.exclude_tags == ['private']

    def test_init_without_uri(self) -> None:
        """Test initialization without required uri field."""
        with pytest.raises(ValidationError):
            AppSettings()  # type: ignore

    def test_model_validate_base_url(self) -> None:
        """Test base_url validation."""
        settings = AppSettings(uri='https://api.example.com/v1')
        assert settings.base_url == 'https://api.example.com'

        settings = AppSettings(uri='https://api.example.com/v1', base_url='https://api.example.com')
        assert settings.base_url == 'https://api.example.com'

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed."""
        settings = AppSettings(uri='http://example.com/api', extra_field='value')  # type: ignore
        assert hasattr(settings, 'extra_field')
        assert settings.extra_field == 'value'

    def test_get_client_config(self) -> None:
        """Test get_client_config method."""
        settings = AppSettings(  # type: ignore
            uri='http://example.com/api',
            base_url='http://api.example.com',
            api_key='test-key',
            token='test-token',  # noqa: S106
            api_key_header='X-API-Key',
            token_header='Auth',  # noqa: S106
            timeout=60,
            include_methods=['GET'],  # Should be excluded from client config
        )

        config = settings.get_client_config()
        assert config['base_url'] == 'http://api.example.com'
        assert config['api_key'] == 'test-key'
        assert config['token'] == 'test-token'  # noqa: S105
        assert config['api_key_header'] == 'X-API-Key'
        assert config['token_header'] == 'Auth'  # noqa: S105
        assert config['timeout'] == 60
        assert 'include_methods' not in config

    def test_get_lookup_config(self) -> None:
        """Test get_lookup_config method."""
        settings = AppSettings(  # type: ignore
            uri='http://example.com/api',
            include_methods=['GET', 'POST'],
            exclude_methods=['DELETE'],
            include_tags=['public'],
            exclude_tags=['private'],
            filters={'path': '/api/v1/.*'},
            api_key='test-key',  # Should be excluded from lookup config
        )

        config = settings.get_lookup_config()
        assert config['include_methods'] == ['GET', 'POST']
        assert config['exclude_methods'] == ['DELETE']
        assert config['include_tags'] == ['public']
        assert config['exclude_tags'] == ['private']
        assert config['filters'] == {'path': '/api/v1/.*'}
        assert 'api_key' not in config
        assert 'uri' not in config


class TestClientSettings:
    """Tests for ClientSettings class."""

    def test_init_with_required_fields(self) -> None:
        """Test initialization with required fields."""
        settings = ClientSettings(name='TestApp', base_url='http://example.com')
        assert settings.name == 'TestApp'
        assert settings.base_url == 'http://example.com'
        assert settings.api_key is None
        assert settings.token is None
        assert settings.api_key_header == 'X-API-Key'
        assert settings.token_header == 'Authorization'  # noqa: S105
        assert settings.timeout == 30

    def test_init_with_optional_fields(self) -> None:
        """Test initialization with optional fields."""
        settings = ClientSettings(
            name='TestApp',
            base_url='http://example.com',
            api_key='test-key',
            token='test-token',  # noqa: S106
            api_key_header='X-Custom-Key',
            token_header='X-Custom-Token',  # noqa: S106
            timeout=60,
        )
        assert settings.name == 'TestApp'
        assert settings.base_url == 'http://example.com'
        assert settings.api_key == 'test-key'
        assert settings.token == 'test-token'  # noqa: S105
        assert settings.api_key_header == 'X-Custom-Key'
        assert settings.token_header == 'X-Custom-Token'  # noqa: S105
        assert settings.timeout == 60

    def test_init_without_required_fields(self) -> None:
        """Test initialization without required fields."""
        with pytest.raises(ValidationError):
            ClientSettings()  # type: ignore

        with pytest.raises(ValidationError):
            ClientSettings(name='TestApp')  # type: ignore

        with pytest.raises(ValidationError):
            ClientSettings(base_url='http://example.com')  # type: ignore

    def test_with_env_prefix(self) -> None:
        """Test creating settings with environment variable prefix."""
        with patch.dict(
            os.environ,
            {
                'APPDOG_TEST_APP_API_KEY': 'env-key',
                'APPDOG_TEST_APP_TOKEN': 'env-token',
                'APPDOG_TEST_APP_TIMEOUT': '45',
            },
        ):
            settings = ClientSettings.with_env_prefix(
                name='TestApp',
                base_url='http://example.com',
            )
            assert settings.name == 'TestApp'
            assert settings.base_url == 'http://example.com'
            assert settings.api_key == 'env-key'
            assert settings.token == 'env-token'  # noqa: S105
            assert settings.timeout == 45

    def test_get_headers_no_auth(self) -> None:
        """Test getting headers without authentication."""
        settings = ClientSettings(name='TestApp', base_url='http://example.com')
        headers = settings.get_headers()
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def test_get_headers_with_api_key(self) -> None:
        """Test getting headers with API key authentication."""
        settings = ClientSettings(
            name='TestApp',
            base_url='http://example.com',
            api_key='test-key',
        )
        headers = settings.get_headers()
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': 'test-key',
        }

    def test_get_headers_with_token(self) -> None:
        """Test getting headers with token authentication."""
        settings = ClientSettings(
            name='TestApp',
            base_url='http://example.com',
            token='test-token',  # noqa: S106
        )
        headers = settings.get_headers()
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
        }

    def test_get_headers_with_both_auth(self) -> None:
        """Test getting headers with both API key and token authentication."""
        settings = ClientSettings(
            name='TestApp',
            base_url='http://example.com',
            api_key='test-key',
            token='test-token',  # noqa: S106
        )
        headers = settings.get_headers()
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': 'test-key',
            'Authorization': 'Bearer test-token',
        }

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed."""
        settings = ClientSettings(  # type: ignore
            name='TestApp',
            base_url='http://example.com',
            extra_field='value',
        )
        assert hasattr(settings, 'extra_field')
        assert settings.extra_field == 'value'


class TestComputeHeaders:
    """Tests for _compute_headers function."""

    def test_compute_headers_no_auth(self) -> None:
        """Test computing headers without authentication."""
        headers = _compute_headers(None, None, 'X-API-Key', 'Authorization')
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def test_compute_headers_with_api_key(self) -> None:
        """Test computing headers with API key authentication."""
        headers = _compute_headers('test-key', None, 'X-API-Key', 'Authorization')
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': 'test-key',
        }

    def test_compute_headers_with_token(self) -> None:
        """Test computing headers with token authentication."""
        headers = _compute_headers(None, 'test-token', 'X-API-Key', 'Authorization')
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
        }

    def test_compute_headers_with_both_auth(self) -> None:
        """Test computing headers with both API key and token authentication."""
        headers = _compute_headers('test-key', 'test-token', 'X-API-Key', 'Authorization')
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': 'test-key',
            'Authorization': 'Bearer test-token',
        }

    def test_compute_headers_custom_headers(self) -> None:
        """Test computing headers with custom header names."""
        headers = _compute_headers(
            'test-key',
            'test-token',
            'X-Custom-Key',
            'X-Custom-Token',
        )
        assert headers == {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Custom-Key': 'test-key',
            'X-Custom-Token': 'Bearer test-token',
        }

    def test_compute_headers_caching(self) -> None:
        """Test that _compute_headers is cached."""
        headers1 = _compute_headers('test-key', 'test-token', 'X-API-Key', 'Authorization')
        headers2 = _compute_headers('test-key', 'test-token', 'X-API-Key', 'Authorization')
        assert headers1 is headers2  # Same object due to caching
