import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from httpx import AsyncClient, Response

from appdog._internal.clients import BaseClient
from appdog._internal.errors import (
    AuthError,
    NotFoundError,
    RateLimitError,
    RequestError,
    ResponseError,
)
from appdog._internal.settings import ClientSettings


class MockResponse:
    """Mock HTTP response for testing."""

    def __init__(
        self,
        status_code: int = 200,
        json_data: dict[str, Any] | None = None,
        is_json: bool = True,
        raise_for_status: bool = False,
    ):
        self.status_code = status_code
        self.json_data = json_data or {}
        self.is_json = is_json
        self._raise_for_status = raise_for_status
        self.content = b'' if status_code == 204 or not is_json else b'{"data": "some content"}'
        self.text = (
            ''
            if status_code == 204
            else ('Not a JSON response' if not is_json else json.dumps(self.json_data))
        )

    def json(self) -> dict[str, Any]:
        """Return JSON data."""
        if not self.is_json:
            raise json.JSONDecodeError('Invalid JSON', 'response', 0)
        return self.json_data

    def raise_for_status(self) -> None:
        """Raise an exception if the status code is not 2xx."""
        if self._raise_for_status:
            raise httpx.HTTPStatusError(
                message=f'HTTP {self.status_code}',
                request=httpx.Request(method='GET', url='https://example.com'),
                response=Response(
                    self.status_code, request=httpx.Request(method='GET', url='https://example.com')
                ),
            )


class TestBaseClient:
    """Tests for BaseClient."""

    @pytest.fixture
    def client(self) -> BaseClient:
        """Create a basic client instance."""
        return BaseClient(name='test', base_url='https://api.example.com')

    @pytest.fixture
    def client_with_auth(self) -> BaseClient:
        """Create a client instance with authentication."""
        return BaseClient(
            name='test',
            base_url='https://api.example.com',
            api_key='test-api-key',
            token='test-token',  # noqa: S106
            timeout=10.0,
        )

    def test_init(self) -> None:
        """Test client initialization."""
        client = BaseClient(name='test', base_url='https://api.example.com')

        assert client._client is None
        assert isinstance(client._settings, ClientSettings)
        assert client._settings.base_url == 'https://api.example.com'

    def test_init_with_auth(self) -> None:
        """Test client initialization with authentication."""
        client = BaseClient(
            name='test',
            base_url='https://api.example.com',
            api_key='test-api-key',
            token='test-token',  # noqa: S106
            api_key_header='X-API-Key',
            token_header='Authorization',  # noqa: S106
            timeout=10.0,
        )

        assert client._client is None
        assert isinstance(client._settings, ClientSettings)
        assert client._settings.base_url == 'https://api.example.com'
        assert client._settings.api_key == 'test-api-key'
        assert client._settings.token == 'test-token'  # noqa: S105
        assert client._settings.api_key_header == 'X-API-Key'
        assert client._settings.token_header == 'Authorization'  # noqa: S105
        assert client._settings.timeout == 10.0

    def test_open(self, client: BaseClient) -> None:
        """Test opening the HTTP client."""
        # Ensure client is initially None
        assert client._client is None

        # Open the client
        client.open()

        # Verify client is now an instance of AsyncClient
        assert isinstance(client._client, AsyncClient)
        assert client._client.base_url == httpx.URL('https://api.example.com')

    async def test_context_manager(self, client: BaseClient) -> None:
        """Test the client as a context manager."""
        # Mock the open and close methods
        with patch.object(client, 'open') as mock_open:
            with patch.object(client, 'close') as mock_close:
                async with client as c:
                    assert c is client
                    assert mock_open.called

                assert mock_close.called

    async def test_close(self) -> None:
        """Test closing the HTTP client."""
        client = BaseClient(name='test', base_url='https://api.example.com')

        # Create a mock client
        mock_http_client = AsyncMock()
        client._client = mock_http_client

        # Close the client
        await client.close()

        # Verify aclose was called and client is None
        assert mock_http_client.aclose.called
        assert client._client is None

    async def test_request_client_not_initialized(self, client: BaseClient) -> None:
        """Test request with uninitialized client."""
        # Mock _create_client to avoid real HTTP requests
        with patch.object(client, '_create_client') as mock_create_client:
            # Mock returns a properly mocked AsyncClient
            mock_client = AsyncMock(spec=AsyncClient)
            mock_client.request.side_effect = httpx.RequestError('Test error')
            mock_create_client.return_value = mock_client

            with pytest.raises(RequestError, match='Request failed'):
                await client._request('GET', '/test')

    async def test_get_request(self, client: BaseClient) -> None:
        """Test GET request."""
        # Set up mock response
        mock_response = MockResponse(
            status_code=200, json_data={'success': True, 'data': {'id': 123, 'name': 'Test'}}
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            response = await client._get('/test', params={'q': 'search'})

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                method='GET',
                url='/test',
                params={'q': 'search'},
                json=None,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )

            # Verify response was parsed correctly
            assert response == {'success': True, 'data': {'id': 123, 'name': 'Test'}}

    async def test_post_request(self, client: BaseClient) -> None:
        """Test POST request."""
        # Set up mock response
        mock_response = MockResponse(status_code=201, json_data={'success': True, 'id': 456})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            data = {'name': 'New Item'}
            response = await client._post('/items', data=data)

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                method='POST',
                url='/items',
                params=None,
                json=data,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )

            # Verify response was parsed correctly
            assert response == {'success': True, 'id': 456}

    async def test_put_request(self, client: BaseClient) -> None:
        """Test PUT request."""
        # Set up mock response
        mock_response = MockResponse(status_code=200, json_data={'success': True, 'id': 123})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            data = {'name': 'Updated Item'}
            response = await client._put('/items/123', data=data)

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                method='PUT',
                url='/items/123',
                params=None,
                json=data,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )

            # Verify response was parsed correctly
            assert response == {'success': True, 'id': 123}

    async def test_patch_request(self, client: BaseClient) -> None:
        """Test PATCH request."""
        # Set up mock response
        mock_response = MockResponse(status_code=200, json_data={'success': True, 'id': 123})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            data = {'status': 'active'}
            response = await client._patch('/items/123', data=data)

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                method='PATCH',
                url='/items/123',
                params=None,
                json=data,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )

            # Verify response was parsed correctly
            assert response == {'success': True, 'id': 123}

    async def test_delete_request(self, client: BaseClient) -> None:
        """Test DELETE request."""
        # Set up mock response for successful delete (204 No Content)
        mock_response = MockResponse(status_code=204, json_data=None, is_json=False)

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            response = await client._delete('/items/123')

            # Verify request was called with correct arguments
            mock_request.assert_called_once_with(
                method='DELETE',
                url='/items/123',
                params=None,
                json=None,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )

            # For 204 responses, we expect either an empty string or an empty dict
            assert response == '' or response == {}

    async def test_request_with_return_type_pydantic(self, client: BaseClient) -> None:
        """Test request with Pydantic model return type."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            id: int
            name: str

        # Set up mock response
        mock_response = MockResponse(status_code=200, json_data={'id': 123, 'name': 'Test'})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            response = await client._get('/items/123', return_type=TestModel)

            # Verify response was parsed correctly
            assert isinstance(response, TestModel)
            assert response.id == 123
            assert response.name == 'Test'

    async def test_request_with_return_type_dataclass(self, client: BaseClient) -> None:
        """Test request with dataclass return type."""
        from dataclasses import dataclass

        @dataclass
        class TestDataClass:
            id: int
            name: str

        # Set up mock response
        mock_response = MockResponse(status_code=200, json_data={'id': 456, 'name': 'Test Data'})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            response = await client._get('/items/456', return_type=TestDataClass)

            # Verify response was parsed correctly
            assert isinstance(response, TestDataClass)
            assert response.id == 456
            assert response.name == 'Test Data'

    async def test_request_with_custom_headers(self, client: BaseClient) -> None:
        """Test request with custom headers."""
        # Set up mock response
        mock_response = MockResponse(status_code=200, json_data={'success': True})

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            custom_headers = {'X-Custom-Header': 'value', 'X-Another-Header': 'another-value'}
            await client._get('/test', headers=custom_headers)

            # Verify request was called with merged headers
            expected_headers = {**client._settings.get_headers(), **custom_headers}
            call_args = mock_request.call_args[1]
            assert call_args['headers'] == expected_headers

    async def test_auth_error_401(self, client: BaseClient) -> None:
        """Test authentication error (401)."""
        # Set up mock response for 401 error
        mock_response = MockResponse(
            status_code=401, json_data={'message': 'Unauthorized'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(AuthError) as exc_info:
                await client._get('/protected')

            assert exc_info.value.status_code == 401
            assert 'Authentication error' in str(exc_info.value)

    async def test_auth_error_403(self, client: BaseClient) -> None:
        """Test authorization error (403)."""
        # Set up mock response for 403 error
        mock_response = MockResponse(
            status_code=403, json_data={'message': 'Forbidden'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(AuthError) as exc_info:
                await client._get('/admin')

            assert exc_info.value.status_code == 403
            assert 'Authentication error' in str(exc_info.value)

    async def test_not_found_error_404(self, client: BaseClient) -> None:
        """Test not found error (404)."""
        # Set up mock response for 404 error
        mock_response = MockResponse(
            status_code=404, json_data={'message': 'Not Found'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(NotFoundError) as exc_info:
                await client._get('/nonexistent')

            assert exc_info.value.status_code == 404
            assert 'Resource not found' in str(exc_info.value)

    async def test_rate_limit_error_429(self, client: BaseClient) -> None:
        """Test rate limit error (429)."""
        # Set up mock response for 429 error
        mock_response = MockResponse(
            status_code=429, json_data={'message': 'Too Many Requests'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(RateLimitError) as exc_info:
                await client._get('/api')

            assert exc_info.value.status_code == 429
            assert 'Rate limit exceeded' in str(exc_info.value)

    async def test_client_error_4xx(self, client: BaseClient) -> None:
        """Test client error (4xx)."""
        # Set up mock response for 400 error
        mock_response = MockResponse(
            status_code=400, json_data={'message': 'Bad Request'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(ResponseError) as exc_info:
                await client._post('/data', data={'invalid': 'data'})

            assert exc_info.value.status_code == 400
            assert 'Client error' in str(exc_info.value)

    async def test_server_error_5xx(self, client: BaseClient) -> None:
        """Test server error (5xx)."""
        # Set up mock response for 500 error
        mock_response = MockResponse(
            status_code=500, json_data={'message': 'Internal Server Error'}, raise_for_status=True
        )

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response):
            with pytest.raises(ResponseError) as exc_info:
                await client._get('/api')

            assert exc_info.value.status_code == 500
            assert 'Server error' in str(exc_info.value)

    async def test_network_error(self, client: BaseClient) -> None:
        """Test network error."""
        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(
            client._client, 'request', side_effect=httpx.RequestError('Connection error')
        ):
            with pytest.raises(RequestError) as exc_info:
                await client._get('/api')

            assert 'Request failed' in str(exc_info.value)

    async def test_json_decode_error(self, client: BaseClient) -> None:
        """Test JSON decode error handling."""
        # Set up mock response with invalid JSON
        mock_response = MockResponse(status_code=200, is_json=False)
        # Add text attribute to mock
        mock_response.text = 'Not a JSON response'

        # Open the client and patch the request method
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request', return_value=mock_response) as mock_request:
            # We expect to get the text response when JSON decoding fails
            response = await client._get('/test')
            assert response == 'Not a JSON response'

            # Verify request was called
            assert mock_request.called

    def test_load(self) -> None:
        """Test loading client from project settings."""
        # Create a mock Project instance
        mock_project = MagicMock()

        # Create mock app settings
        mock_settings = MagicMock()
        mock_settings.get_client_config.return_value = {
            'base_url': 'https://api.example.com',
            'api_key': 'test-key',
            'token': 'test-token',
            'api_key_header': 'X-Custom-Key',
            'token_header': 'X-Custom-Auth',
            'timeout': 60,
        }

        # Set up project settings
        mock_project.settings = {'test_app': mock_settings}

        # Mock Project.load to return our mock project
        with patch('appdog._internal.clients.Project.load', return_value=mock_project):
            # Test loading existing app
            client = BaseClient.load('test_app')

            # Verify client was configured correctly
            assert client._settings.name == 'test_app'
            assert client._settings.base_url == 'https://api.example.com'
            assert client._settings.api_key == 'test-key'
            assert client._settings.token == 'test-token'  # noqa: S105
            assert client._settings.api_key_header == 'X-Custom-Key'
            assert client._settings.token_header == 'X-Custom-Auth'  # noqa: S105
            assert client._settings.timeout == 60

            # Test loading non-existing app
            with pytest.raises(ValueError):
                BaseClient.load('non_existing_app')

    async def test_path_normalization(self, client: BaseClient) -> None:
        """Test path normalization."""
        # Mock request
        client.open()
        assert client._client is not None

        with patch.object(client._client, 'request') as mock_request:
            # Create mock response
            mock_request.return_value = MockResponse(status_code=200, json_data={'data': 'value'})

            # Call with path missing leading slash
            await client._get('test')

            # Verify path was normalized
            mock_request.assert_called_once_with(
                method='GET',
                url='/test',
                params=None,
                json=None,
                headers=client._settings.get_headers(),
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0),
            )
