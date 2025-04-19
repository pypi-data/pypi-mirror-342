from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from appdog._internal.managers import project_manager, registry_manager
from appdog._internal.project import Project
from appdog._internal.registry import Registry


class TestProjectManager:
    """Tests for project manager."""

    @pytest.fixture
    def project_dir(self) -> Path:
        """Create a test project directory path."""
        return Path('/test/project')

    @pytest.fixture
    def registry_dir(self) -> Path:
        """Create a test registry directory path."""
        return Path('/test/registry')

    @pytest.fixture
    def mock_project_manager(self) -> MagicMock:
        """Create a mock Project instance."""
        project_mock = MagicMock(spec=Project)
        project_mock.__aenter__ = AsyncMock(return_value=project_mock)
        project_mock.__aexit__ = AsyncMock(return_value=None)
        return project_mock

    @pytest.fixture
    def mock_project(self) -> MagicMock:
        """Create a mock Project instance."""
        project_mock = MagicMock(spec=Project)
        project_mock.__aenter__ = AsyncMock(return_value=project_mock)
        project_mock.__aexit__ = AsyncMock(return_value=None)
        return project_mock

    async def test_project_manager_with_dirs(
        self, project_dir: Path, registry_dir: Path, mock_project: MagicMock
    ) -> None:
        """Test project manager with specific directories."""
        # Patch Project.load to return our mock
        with patch('appdog._internal.managers.Project.load', return_value=mock_project) as mock_load:
            # Use the project manager as a context manager
            async with project_manager(project_dir, registry_dir) as context:
                # Verify Project.load was called with correct arguments
                mock_load.assert_called_once_with(project_dir, registry_dir)
                # Verify the context manager returned our mock
                assert context is mock_project
                # Verify __aenter__ was called
                assert mock_project.__aenter__.called

            # Verify __aexit__ was called when exiting the context
            assert mock_project.__aexit__.called

    async def test_project_manager_default_dirs(self, mock_project: MagicMock) -> None:
        """Test project manager with default directories."""
        # Patch Project.load to return our mock
        with patch('appdog._internal.managers.Project.load', return_value=mock_project) as mock_load:
            # Use the project manager with default directories
            async with project_manager() as context:
                # Verify Project.load was called with None for both directories
                mock_load.assert_called_once_with(None, None)
                # Verify the context manager returned our mock
                assert context is mock_project

            # Verify __aexit__ was called when exiting the context
            assert mock_project.__aexit__.called

    async def test_project_manager_exception(self, mock_project: MagicMock) -> None:
        """Test project manager handling exceptions."""
        # Patch Project.load to return our mock
        with patch('appdog._internal.managers.Project.load', return_value=mock_project):
            # Use the project manager as a context manager with an exception
            with pytest.raises(RuntimeError, match='Test exception'):
                async with project_manager() as _:
                    raise RuntimeError('Test exception')

            # Verify __aexit__ was called with the exception information
            assert mock_project.__aexit__.called
            # Get the first call arguments (exception info)
            call_args = mock_project.__aexit__.call_args[0]
            # Verify first argument is the exception type
            assert call_args[0] is RuntimeError


class TestRegistryManager:
    """Tests for registry manager."""

    @pytest.fixture
    def registry_dir(self) -> Path:
        """Create a test registry directory path."""
        return Path('/test/registry')

    @pytest.fixture
    def mock_registry_manager(self) -> MagicMock:
        """Create a mock Registry instance."""
        registry_mock = MagicMock(spec=Registry)
        registry_mock.__aenter__ = AsyncMock(return_value=registry_mock)
        registry_mock.__aexit__ = AsyncMock(return_value=None)
        return registry_mock

    @pytest.fixture
    def mock_registry(self) -> MagicMock:
        """Create a mock Registry instance."""
        registry_mock = MagicMock(spec=Registry)
        registry_mock.__aenter__ = AsyncMock(return_value=registry_mock)
        registry_mock.__aexit__ = AsyncMock(return_value=None)
        return registry_mock

    async def test_registry_manager_with_dir(
        self, registry_dir: Path, mock_registry: MagicMock
    ) -> None:
        """Test registry manager with specific directory."""
        # Patch Registry.load to return our mock
        with patch(
            'appdog._internal.managers.Registry.load', return_value=mock_registry
        ) as mock_load:
            # Use the registry manager as a context manager
            async with registry_manager(registry_dir) as context:
                # Verify Registry.load was called with correct arguments
                mock_load.assert_called_once_with(registry_dir)
                # Verify the context manager returned our mock
                assert context is mock_registry
                # Verify __aenter__ was called
                assert mock_registry.__aenter__.called

            # Verify __aexit__ was called when exiting the context
            assert mock_registry.__aexit__.called

    async def test_registry_manager_default_dir(self, mock_registry: MagicMock) -> None:
        """Test registry manager with default directory."""
        # Patch Registry.load to return our mock
        with patch(
            'appdog._internal.managers.Registry.load', return_value=mock_registry
        ) as mock_load:
            # Use the registry manager with default directory
            async with registry_manager() as context:
                # Verify Registry.load was called with None for directory
                mock_load.assert_called_once_with(None)
                # Verify the context manager returned our mock
                assert context is mock_registry

            # Verify __aexit__ was called when exiting the context
            assert mock_registry.__aexit__.called

    async def test_registry_manager_exception(self, mock_registry: MagicMock) -> None:
        """Test registry manager handling exceptions."""
        # Patch Registry.load to return our mock
        with patch('appdog._internal.managers.Registry.load', return_value=mock_registry):
            # Use the registry manager as a context manager with an exception
            with pytest.raises(RuntimeError, match='Test exception'):
                async with registry_manager() as _:
                    raise RuntimeError('Test exception')

            # Verify __aexit__ was called with the exception information
            assert mock_registry.__aexit__.called
            # Get the first call arguments (exception info)
            call_args = mock_registry.__aexit__.call_args[0]
            # Verify first argument is the exception type
            assert call_args[0] is RuntimeError
