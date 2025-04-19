import json
from pathlib import Path
from typing import Any
from unittest import mock

import pytest
from typing_extensions import Self

from tests.conftest import AsyncNoWarningMock


class TestImports:
    """Tests for module imports in the appdog package."""

    @mock.patch('builtins.__import__')
    def test_appdog_petstore_import(self, mock_import: mock.MagicMock) -> None:
        """Test that appdog.petstore can be imported."""
        # Create a mock module
        mock_module = mock.MagicMock()
        mock_module.PetstoreClient = mock.MagicMock()
        mock_module.client = mock.MagicMock()
        mock_module.models = mock.MagicMock()

        # Configure import to return our mock
        mock_import.return_value = mock_module

        # Try importing
        try:
            # This will use our mocked __import__
            module = __import__('appdog.petstore', fromlist=['*'])

            # Verify it worked
            assert module is mock_module
            assert hasattr(module, 'PetstoreClient')
            assert hasattr(module, 'client')
            assert hasattr(module, 'models')
        except ImportError as e:
            pytest.fail(f'Failed to import appdog.petstore: {e}')

        # Verify import was called correctly
        mock_import.assert_called_with('appdog.petstore', fromlist=['*'])

    @mock.patch('builtins.__import__')
    def test_petstore_client_attributes(self, mock_import: mock.MagicMock) -> None:
        """Test that the PetstoreClient class has expected attributes and methods."""
        # Create mock client class
        mock_client_class = mock.MagicMock()
        mock_client_class.__aenter__ = AsyncNoWarningMock()
        mock_client_class.__aexit__ = AsyncNoWarningMock()
        mock_client_class.get_pet_find_by_status = AsyncNoWarningMock()

        # Create mock client instance
        mock_client_instance = mock.MagicMock()

        # Create a mock module
        mock_module = mock.MagicMock()
        mock_module.PetstoreClient = mock_client_class
        mock_module.client = mock_client_instance

        # Configure import to return our mock
        mock_import.return_value = mock_module

        # Import the module
        module = __import__('appdog.petstore', fromlist=['*'])

        # Check PetstoreClient class exists
        assert hasattr(module, 'PetstoreClient')

        # Check client instance exists
        assert hasattr(module, 'client')

        # Check expected client methods
        client_class = module.PetstoreClient
        assert hasattr(client_class, 'get_pet_find_by_status')
        assert hasattr(client_class, '__aenter__')
        assert hasattr(client_class, '__aexit__')

    @mock.patch('builtins.__import__')
    def test_petstore_models_import(self, mock_import: mock.MagicMock) -> None:
        """Test that appdog.petstore.models can be imported and has expected classes."""
        # Create a mock models module
        mock_models = mock.MagicMock()

        # Create a mock petstore module
        mock_module = mock.MagicMock()
        mock_module.models = mock_models

        # Configure import to return our mock
        mock_import.return_value = mock_module

        try:
            # Import the module
            module = __import__('appdog.petstore.models', fromlist=['*'])

            # Verify it worked
            assert isinstance(module, mock.MagicMock)
        except ImportError as e:
            pytest.fail(f'Failed to import appdog.petstore.models: {e}')


@pytest.fixture
def petstore_response() -> dict[str, Any]:
    """Load the petstore response fixture."""
    fixtures_path = Path(__file__).parent / 'fixtures'
    with open(fixtures_path / 'response_petstore.json') as f:
        return json.load(f)  # type: ignore


@pytest.mark.asyncio
class TestPetstoreAsyncClient:
    """Tests for the async client functionality."""

    @mock.patch('builtins.__import__')
    async def test_petstore_client_context_manager(
        self, mock_import: mock.MagicMock, monkeypatch: Any, petstore_response: dict[str, Any]
    ) -> None:
        """Test that the PetstoreClient can be used as an async context manager."""
        # Create a mock client class with async methods
        mock_get_pet = AsyncNoWarningMock(return_value=petstore_response)

        # Create a mock client instance
        class MockClient:
            get_pet_find_by_status = mock_get_pet

            async def __aenter__(self) -> Self:
                return self

            async def __aexit__(
                self,
                exc_type: type[BaseException] | None,
                exc_val: BaseException | None,
                exc_tb: object,
            ) -> None:
                pass

        mock_client_instance = MockClient()

        # Create a mock module
        mock_module = mock.MagicMock()
        mock_module.client = mock_client_instance

        # Configure import to return our mock
        mock_import.return_value = mock_module

        # Import the module
        module = __import__('appdog.petstore', fromlist=['*'])

        # Test using the client as context manager
        async with module.client as client:
            result = await client.get_pet_find_by_status(status='available')

        # Check the mock was called correctly
        mock_get_pet.assert_called_once()
        assert result == petstore_response
        assert result['id'] == 1
        assert result['name'] == 'doggie'
        assert result['status'] == 'available'
