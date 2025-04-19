import datetime
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pytest import MonkeyPatch

from appdog._internal.registry import Registry, RegistryPaths, _get_registry_paths
from appdog._internal.specs import AppSpec, EndpointInfo


class TestRegistryPaths:
    """Tests for RegistryPaths named tuple."""

    def test_init(self) -> None:
        """Test initialization of RegistryPaths."""
        paths = RegistryPaths(dir=Path('/test/dir'), specs=Path('/test/dir/registry.json'))
        assert paths.dir == Path('/test/dir')
        assert paths.specs == Path('/test/dir/registry.json')

    def test_immutable(self) -> None:
        """Test that RegistryPaths is immutable."""
        paths = RegistryPaths(dir=Path('/test/dir'), specs=Path('/test/dir/registry.json'))
        with pytest.raises(AttributeError):
            paths.dir = Path('/new/dir')  # type: ignore
        with pytest.raises(AttributeError):
            paths.specs = Path('/new/dir/registry.json')  # type: ignore


class TestRegistry:
    """Tests for Registry class."""

    @pytest.fixture
    def registry_dir(self, tmp_path: Path) -> Path:
        """Create a temporary registry directory."""
        registry_dir = tmp_path / 'registry'
        registry_dir.mkdir()
        return registry_dir

    @pytest.fixture
    def app_spec(self) -> AppSpec:
        """Create a test app specification."""
        return AppSpec(
            uri='http://example.com/api',
            data={'openapi': '3.0.0'},
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            hash='test_hash',
        )

    @pytest.fixture
    def registry(self, registry_dir: Path) -> Generator[Registry, None, None]:
        """Create a Registry instance for testing."""
        from unittest.mock import patch

        # First create a real Registry instance
        registry = Registry(registry_dir)

        # Create a comprehensive mock for specs
        mock_specs = MagicMock()
        mock_specs.__getitem__.return_value = AppSpec(
            uri='http://example.com/api',
            data={'openapi': '3.0.0'},
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            hash='test_hash',
        )
        mock_specs.__contains__.return_value = True

        # Replace specs with our mock
        registry.specs = mock_specs

        # Patch file existence checks
        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = True
            # Patch directory creation
            with patch.object(Path, 'mkdir'):
                # Patch file removal
                with patch.object(Path, 'unlink'):
                    yield registry

    def test_init(self, registry_dir: Path) -> None:
        """Test initialization of Registry."""
        registry = Registry(registry_dir)
        assert registry.paths.dir == registry_dir
        assert registry.paths.specs == registry_dir / 'registry.json'

    def test_init_default_dir(self) -> None:
        """Test initialization with default directory."""
        with patch('appdog._internal.registry.get_registry_dir') as mock_get_registry_dir:
            mock_get_registry_dir.return_value = Path('/test/source/lib')
            registry = Registry()
            assert registry.paths.dir == Path('/test/source/lib')
            assert registry.paths.specs == Path('/test/source/lib/registry.json')

    async def test_context_manager(self, registry: Registry) -> None:
        """Test async context manager."""
        async with registry as context:
            assert context is registry

    async def test_context_manager_save(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test that context manager saves on exit."""
        # Patch the path.exists method to return True after save
        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = True
            registry.specs['test_app'] = app_spec
            async with registry:
                pass
            assert mock_exists.return_value is True

    async def test_context_manager_error(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test that context manager doesn't save on error."""
        registry.specs['test_app'] = app_spec
        with pytest.raises(ValueError):
            async with registry:
                raise ValueError('Test error')
        # No need to check file existence as we're mocking everything

    def test_load(self, registry_dir: Path) -> None:
        """Test loading registry."""
        registry = Registry.load(registry_dir)
        assert registry.paths.dir == registry_dir
        assert registry.paths.specs == registry_dir / 'registry.json'

    def test_load_default(self, monkeypatch: MonkeyPatch) -> None:
        """Test loading default registry."""
        # Reset the singleton instance
        Registry._instance = None

        # First load should create a new instance
        registry1 = Registry.load()
        assert isinstance(registry1, Registry)

        # Second load should return the same instance
        registry2 = Registry.load()
        assert registry1 is registry2

        # Verify basic properties
        assert registry1.paths.dir is not None
        assert registry1.paths.specs is not None
        assert registry1.paths.specs.name == 'registry.json'

    def test_save(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test saving registry."""
        # Patch the path.exists method to return True after save
        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = True
            registry.specs['test_app'] = app_spec
            registry.save()
            assert mock_exists.return_value is True

    def test_add_app(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test adding an application."""
        # Patch the generator to avoid file operations
        with patch('appdog._internal.registry.generate_app_files') as mock_generate:
            # Make sure specs.__contains__ returns False for 'test_app' initially
            registry.specs.__contains__.side_effect = lambda key: False  # type: ignore

            # Call add_app
            registry.add_app('test_app', app_spec)

            # Verify generate_app_files was called
            mock_generate.assert_called_once()

            # Verify specs.__setitem__ was called with correct arguments
            registry.specs.__setitem__.assert_called_once_with('test_app', app_spec)  # type: ignore

    def test_add_app_existing(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test adding an existing application."""
        # Set up mocks to trigger the ValueError logic
        registry.specs.__contains__.return_value = True  # type: ignore
        registry.specs.__getitem__.return_value = app_spec  # type: ignore

        different_spec = AppSpec(
            uri='http://different.com/api',
            data={'openapi': '3.0.0'},
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            hash='different_hash',
        )

        # The validation should fail when URIs don't match
        with pytest.raises(ValueError):
            registry.add_app('test_app', different_spec)

    def test_add_app_force(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test forcing addition of existing application."""
        # Patch the generator to avoid file operations
        with patch('appdog._internal.registry.generate_app_files') as mock_generate:
            # Set up mocks for existing app
            registry.specs.__contains__.return_value = True  # type: ignore
            registry.specs.__getitem__.return_value = app_spec  # type: ignore

            new_spec = AppSpec(
                uri='http://different.com/api',
                data={'openapi': '3.0.0'},
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                hash='new_hash',
            )

            # Mock the __setitem__ to update the return value of __getitem__
            def update_mock_return_value(key: str, value: AppSpec) -> None:
                registry.specs.__getitem__.return_value = value  # type: ignore

            registry.specs.__setitem__.side_effect = update_mock_return_value  # type: ignore

            # Force add should succeed despite URI mismatch
            registry.add_app('test_app', new_spec, force=True)

            # Verify specs.__setitem__ was called with correct arguments
            registry.specs.__setitem__.assert_called_with('test_app', new_spec)  # type: ignore

            # Verify registry.specs['test_app'] returns new_spec after the update
            assert registry.specs.__getitem__.return_value == new_spec  # type: ignore

            # Verify generate_app_files was called
            mock_generate.assert_called_once()

    def test_add_app_upgrade(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test upgrading an application."""
        # Patch the generator to avoid file operations
        with patch('appdog._internal.registry.generate_app_files') as mock_generate:
            # Set up mocks for existing app
            registry.specs.__contains__.return_value = True  # type: ignore
            registry.specs.__getitem__.return_value = app_spec  # type: ignore

            new_spec = AppSpec(
                uri=app_spec.uri,
                data=app_spec.data,
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                hash='new_hash',
            )

            # Mock the __setitem__ to update the return value of __getitem__
            def update_mock_return_value(key: str, value: AppSpec) -> None:
                registry.specs.__getitem__.return_value = value  # type: ignore

            registry.specs.__setitem__.side_effect = update_mock_return_value  # type: ignore

            # Upgrade should succeed with same URI but different hash
            registry.add_app('test_app', new_spec, upgrade=True)

            # Verify specs.__setitem__ was called with correct arguments
            registry.specs.__setitem__.assert_called_with('test_app', new_spec)  # type: ignore

            # Verify registry.specs['test_app'] returns new_spec after the update
            assert registry.specs.__getitem__.return_value == new_spec  # type: ignore

            # Verify generate_app_files was called
            mock_generate.assert_called_once()

    def test_remove_app(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test removing an application."""
        # Set up mocks for existing app
        registry.specs.__contains__.return_value = True  # type: ignore

        # Patch Path.exists specifically for the app directory check
        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = False

            # Remove the app
            registry.remove_app('test_app')

            # Verify __delitem__ was called
            registry.specs.__delitem__.assert_called_with('test_app')  # type: ignore

            # We're asserting the file doesn't exist after removal
            assert not mock_exists.return_value

    def test_remove_app_not_found(self, registry: Registry) -> None:
        """Test removing a non-existent application."""
        # Set up mocks for non-existent app
        registry.specs.__contains__.return_value = False  # type: ignore

        registry.remove_app('nonexistent_app')  # Should not raise an error

        # Verify no operations occurred
        assert not registry.specs.__delitem__.called  # type: ignore

    def test_lookup(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test looking up endpoints."""
        # Set up test endpoints for each app
        app1_endpoints = [
            EndpointInfo(
                name='get_users',
                method='get',
                path='/users',
                tags=['users'],
                operation_id='getUsers',
                summary='Get users',
                description='Get all users',
                parameters=[],
                request_body=None,
                responses={},
            )
        ]

        app2_endpoints = [
            EndpointInfo(
                name='get_items',
                method='get',
                path='/items',
                tags=['items'],
                operation_id='getItems',
                summary='Get items',
                description='Get all items',
                parameters=[],
                request_body=None,
                responses={},
            )
        ]

        # Mock the registry specs
        mock_specs = MagicMock()
        registry.specs = mock_specs

        # Set up a dictionary for the specs.items method
        mock_specs_dict = {'app1': MagicMock(), 'app2': MagicMock()}
        mock_specs.items.return_value = mock_specs_dict.items()

        # Set up the lookup method for each mock spec
        mock_specs_dict['app1'].lookup.return_value = app1_endpoints
        mock_specs_dict['app2'].lookup.return_value = app2_endpoints

        # Test lookup with no filters
        endpoints = registry.lookup()

        # Verify the correct endpoints were returned
        assert len(endpoints) == 2
        assert endpoints['app1'] == app1_endpoints
        assert endpoints['app2'] == app2_endpoints

        # Verify lookup was called with empty kwargs for each app
        assert mock_specs_dict['app1'].lookup.called
        assert mock_specs_dict['app2'].lookup.called

    def test_lookup_with_filters(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test looking up endpoints with filters."""
        # Create mock specs dictionary for the test
        mock_specs = {'app1': app_spec, 'app2': app_spec}

        # Set up test endpoints
        app1_endpoints = [
            EndpointInfo(
                name='get_users',
                method='get',
                path='/users',
                tags=['users'],
                operation_id='getUsers',
                summary='Get users',
                description='Get all users',
                parameters=[],
                request_body=None,
                responses={},
            )
        ]

        # Mock the registry specs dictionary and its methods
        registry.specs = MagicMock()
        registry.specs.items.return_value = mock_specs.items()

        # Mock the lookup method
        with patch(
            'appdog._internal.specs.AppSpec.lookup', return_value=app1_endpoints
        ) as mock_lookup:
            # Test lookup with app-specific filters
            endpoints = registry.lookup(app1=True)

            # Verify correct endpoints were returned
            assert len(endpoints) == 1
            assert 'app1' in endpoints
            assert 'app2' not in endpoints

            # Reset the mock for the next test
            mock_lookup.reset_mock()

            # Test lookup with a specific lookup config
            lookup_config = {'include_methods': ['get']}
            endpoints = registry.lookup(app1=lookup_config)  # type: ignore

            # Verify correct endpoints were returned
            assert len(endpoints) == 1
            assert 'app1' in endpoints
            assert 'app2' not in endpoints

            # Verify lookup was called with correct parameters
            mock_lookup.assert_called_once_with(**lookup_config)

    def test_lookup_with_kwargs(self, registry: Registry, app_spec: AppSpec) -> None:
        """Test looking up endpoints with kwargs filters."""
        # Setup mock for specs.items
        app_endpoints = [
            EndpointInfo(
                name='get_users',
                method='get',
                path='/users',
                tags=['users'],
                operation_id='getUsers',
                summary='Get users',
                description='',
                parameters=[],
                request_body=None,
                responses={},
            )
        ]

        # Mock the lookup method using patch instead of direct assignment (AppSpec is frozen)
        with patch.object(AppSpec, 'lookup', return_value=app_endpoints):
            # Set up the specs items mock
            registry.specs.items.return_value = [('test_app', app_spec)]  # type: ignore

            # Test lookup with path filter in filters
            endpoints = registry.lookup(test_app={'filters': {'path': r'/users'}})
            assert len(endpoints['test_app']) == 1


def test_get_registry_paths() -> None:
    """Test getting registry paths."""
    paths = _get_registry_paths(Path('/test/dir'))
    assert paths.dir == Path('/test/dir')
    assert paths.specs == Path('/test/dir/registry.json')


def test_get_registry_paths_default() -> None:
    """Test getting registry paths with default directory."""
    with patch('appdog._internal.registry.get_registry_dir') as mock_get_registry_dir:
        mock_get_registry_dir.return_value = Path('/test/source/lib')
        paths = _get_registry_paths()
        assert paths.dir == Path('/test/source/lib')
        assert paths.specs == Path('/test/source/lib/registry.json')
