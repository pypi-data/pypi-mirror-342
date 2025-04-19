from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from appdog._internal.cli import app
from appdog._internal.project import Project
from appdog._internal.settings import AppSettings
from tests.conftest import AsyncNoWarningMock


@pytest.fixture
def runner() -> CliRunner:
    """Create a Typer CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_project() -> Generator[MagicMock, None, None]:
    """Mock Project class for testing."""
    with patch('appdog._internal.cli.Project') as mock:
        mock_instance = mock.return_value
        mock_instance.paths.settings.exists.return_value = False
        yield mock_instance


@pytest.fixture
def mock_project_load() -> Generator[MagicMock, None, None]:
    """Mock Project.load method."""
    with patch('appdog._internal.cli.Project.load') as mock:
        yield mock


@pytest.fixture
def mock_asyncio_run() -> Generator[MagicMock, None, None]:
    """Mock asyncio.run to create a clean boundary for testing."""
    with patch('appdog._internal.cli.asyncio.run') as mock:
        # Set a return value that matches test expectations
        mock.return_value = None
        yield mock


@pytest.fixture
def mock_logger() -> Generator[MagicMock, None, None]:
    """Mock the logger to capture log messages."""
    with patch('appdog._internal.cli.logger') as mock_logger:
        yield mock_logger


@pytest.fixture(autouse=True)
def patch_async_functions() -> Generator[dict[str, AsyncNoWarningMock], None, None]:
    """
    Patch all async functions to prevent 'never awaited' warnings.

    Uses custom AsyncNoWarningMock to avoid the coroutine warnings that occur with
    standard mocks.
    """
    # Create our custom mocks for each async function
    mocks = {}
    patches = []

    for func_name in [
        '_add_app_process',
        '_remove_app_process',
        '_lock_process',
        '_sync_process',
    ]:
        # Create a simple mock that doesn't return a coroutine
        mock = AsyncNoWarningMock(return_value=None)
        mocks[func_name] = mock

        # Create and start the patch
        p = patch(f'appdog._internal.cli.{func_name}', mock)
        patches.append(p)
        p.start()

    yield mocks

    # Clean up all patches
    for p in patches:
        p.stop()


class TestCliInit:
    """Tests for init command."""

    def test_init_success(
        self, runner: CliRunner, mock_project: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test successful initialization."""
        result = runner.invoke(app, ['init'])

        assert result.exit_code == 0
        mock_logger.info.assert_any_call('Successfully initialized project in current directory')
        mock_project.save.assert_called_once()

    def test_init_exists(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test initialization when config already exists."""
        with patch('appdog._internal.cli.Project') as mock_project_cls:
            mock_instance = mock_project_cls.return_value
            mock_instance.paths.settings.exists.return_value = True

            result = runner.invoke(app, ['init'])

            assert result.exit_code == 1
            mock_logger.error.assert_any_call('Project already exists. Use `--force` to overwrite.')
            mock_instance.save.assert_not_called()

    def test_init_force(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test forced initialization when config already exists."""
        with patch('appdog._internal.cli.Project') as mock_project_cls:
            mock_instance = mock_project_cls.return_value
            mock_instance.paths.settings.exists.return_value = True

            result = runner.invoke(app, ['init', '--force'])

            assert result.exit_code == 0
            mock_logger.info.assert_any_call(
                'Successfully initialized project in current directory'
            )
            mock_instance.save.assert_called_once()

    def test_init_custom_dir(self, runner: CliRunner) -> None:
        """Test initialization with custom directory."""
        with patch('appdog._internal.cli.Project') as mock_project_cls:
            mock_instance = mock_project_cls.return_value
            mock_instance.paths.settings.exists.return_value = False

            result = runner.invoke(app, ['init', '--project', '/custom/dir'])

            assert result.exit_code == 0
            mock_project_cls.assert_called_once_with(project_dir=Path('/custom/dir'))


class TestCliAdd:
    """Tests for add command."""

    def test_add_success(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test successful app addition."""
        result = runner.invoke(
            app,
            [
                'add',
                'test-app',
                '--uri',
                'http://example.com/api',
                '--base-url',
                'http://example.com',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call("Successfully added project application 'test-app'")

    def test_add_with_options(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test app addition with various options."""
        result = runner.invoke(
            app,
            [
                'add',
                'test-app',
                '--uri',
                'http://example.com/api',
                '--include-methods',
                'GET',
                '--include-methods',
                'POST',
                '--exclude-tags',
                'internal',
                '--force',
                '--frozen',
                '--upgrade',
                '--sync',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call("Successfully added project application 'test-app'")

    def test_add_error(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test app addition error handling."""
        mock_asyncio_run.side_effect = ValueError('Test error')

        result = runner.invoke(
            app,
            [
                'add',
                'test-app',
                '--uri',
                'http://example.com/api',
            ],
        )

        assert result.exit_code == 1
        mock_logger.error.assert_any_call('Failed to add project application: Test error')


class TestCliRemove:
    """Tests for remove command."""

    def test_remove_success(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test successful app removal."""
        result = runner.invoke(
            app,
            [
                'remove',
                'test-app',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call("Successfully removed project application 'test-app'")

    def test_remove_with_options(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test app removal with options."""
        result = runner.invoke(
            app,
            [
                'remove',
                'test-app',
                '--frozen',
                '--sync',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call("Successfully removed project application 'test-app'")

    def test_remove_error(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test app removal error handling."""
        mock_asyncio_run.side_effect = ValueError('Test error')

        result = runner.invoke(
            app,
            [
                'remove',
                'test-app',
            ],
        )

        assert result.exit_code == 1
        mock_logger.error.assert_any_call('Failed to remove project application: Test error')


class TestCliList:
    """Tests for list command."""

    def test_list_success(self, runner: CliRunner) -> None:
        """Test successful listing of appdog."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_project = MagicMock(spec=Project)
            mock_load.return_value = mock_project

            # Mock settings dictionary with appdog
            mock_project.settings = {
                'app1': MagicMock(spec=AppSettings, uri='http://example.com/api1'),
                'app2': MagicMock(spec=AppSettings, uri='http://example.com/api2'),
            }

            result = runner.invoke(app, ['list'])

            assert result.exit_code == 0

    def test_list_empty(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test listing with no appdog."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_project = MagicMock(spec=Project)
            mock_project.settings = {}
            mock_load.return_value = mock_project

            result = runner.invoke(app, ['list'])

            assert result.exit_code == 0
            mock_logger.warning.assert_any_call('No project applications registered')

    def test_list_error(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test listing error handling."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_load.side_effect = FileNotFoundError('Test error')

            result = runner.invoke(app, ['list'])

            assert result.exit_code == 1
            mock_logger.error.assert_any_call('Failed to list project applications: Test error')


class TestCliLock:
    """Tests for lock command."""

    def test_lock_success(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test successful lock."""
        result = runner.invoke(app, ['lock'])

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call('Successfully locked project specifications')

    def test_lock_with_options(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test lock with options."""
        result = runner.invoke(
            app,
            [
                'lock',
                '--force',
                '--upgrade',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call('Successfully locked project specifications')

    def test_lock_error(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test lock error handling."""
        mock_asyncio_run.side_effect = ValueError('Test error')

        result = runner.invoke(app, ['lock'])

        assert result.exit_code == 1
        mock_logger.error.assert_any_call('Failed to lock project specifications: Test error')


class TestCliSync:
    """Tests for sync command."""

    def test_sync_success(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test successful sync."""
        result = runner.invoke(app, ['sync'])

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call('Successfully synced applications with project registry')

    def test_sync_with_options(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test sync with options."""
        result = runner.invoke(
            app,
            [
                'sync',
                '--force',
                '--frozen',
                '--upgrade',
            ],
        )

        mock_asyncio_run.assert_called_once()
        assert result.exit_code == 0
        mock_logger.info.assert_any_call('Successfully synced applications with project registry')

    def test_sync_error(
        self, runner: CliRunner, mock_asyncio_run: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Test sync error handling."""
        mock_asyncio_run.side_effect = ValueError('Test error')

        result = runner.invoke(app, ['sync'])

        assert result.exit_code == 1
        mock_logger.error.assert_any_call('Failed to sync applications: Test error')


class TestCliMCP:
    """Tests for MCP command."""

    def test_mcp_run_success(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test successful MCP run command execution."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            result = runner.invoke(
                app,
                [
                    'mcp',
                    'run',
                    '--name',
                    'Test Server',
                ],
            )

            assert result.exit_code == 0
            mock_mcp.assert_called_once_with(
                name='Test Server',
                project_dir=None,
                mode='run',
                force=False,
                transport='stdio',  # Default value for run command
                output=None,
            )
            mock_logger.info.assert_any_call('Run MCP applications in production mode...')

    def test_mcp_install_with_options(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test MCP install command with various options."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            result = runner.invoke(
                app,
                [
                    'mcp',
                    'install',
                    '--name',
                    'API Server',
                    '--force',
                    '-v',
                    'API_KEY=123',
                    '-f',
                    '.env',
                    '--project',
                    '/custom/dir',
                    '--output',
                    'server.py',
                ],
            )

            assert result.exit_code == 0
            mock_mcp.assert_called_once_with(
                name='API Server',
                project_dir=Path('/custom/dir'),
                mode='install',
                force=True,
                env_vars=['API_KEY=123'],
                env_file=Path('.env'),
                with_packages=None,
                with_editable=None,
                output=Path('server.py'),
            )
            mock_logger.info.assert_any_call('Install applications in MCP client...')

    def test_mcp_install_error(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test MCP install command error handling."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            mock_mcp.side_effect = ValueError('Test error')

            result = runner.invoke(
                app,
                [
                    'mcp',
                    'install',
                ],
            )

            assert result.exit_code == 1
            mock_logger.error.assert_any_call('Failed to process MCP install mode: Test error')

    def test_mcp_dev_with_options(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test MCP dev command with options."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            result = runner.invoke(
                app,
                [
                    'mcp',
                    'dev',
                    '--name',
                    'Dev Server',
                    '--with',
                    'pandas',
                    '--with',
                    'numpy',
                    '--with-editable',
                    '.',
                ],
            )

            assert result.exit_code == 0
            mock_mcp.assert_called_once_with(
                name='Dev Server',
                project_dir=None,
                mode='dev',
                force=False,
                with_packages=['pandas', 'numpy'],
                with_editable=Path('.'),
                output=None,
            )
            mock_logger.info.assert_any_call(
                'Run MCP applications in development mode with inspector...'
            )

    def test_mcp_install_with_env_vars(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test MCP install command with environment variables."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            result = runner.invoke(
                app,
                [
                    'mcp',
                    'install',
                    '--name',
                    'Install Server',
                    '-v',
                    'API_KEY=abc123',
                    '-f',
                    '.env',
                ],
            )

            assert result.exit_code == 0
            mock_mcp.assert_called_once_with(
                name='Install Server',
                project_dir=None,
                mode='install',
                force=False,
                env_vars=['API_KEY=abc123'],
                env_file=Path('.env'),
                with_packages=None,
                with_editable=None,
                output=None,
            )
            mock_logger.info.assert_any_call('Install applications in MCP client...')

    def test_mcp_run_with_transport(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test MCP run command with transport option."""
        with patch('appdog._internal.cli._mcp_process') as mock_mcp:
            result = runner.invoke(
                app,
                [
                    'mcp',
                    'run',
                    '--name',
                    'Run Server',
                    '--transport',
                    'sse',
                ],
            )

            assert result.exit_code == 0
            mock_mcp.assert_called_once_with(
                name='Run Server',
                project_dir=None,
                mode='run',
                force=False,
                transport='sse',
                output=None,
            )
            mock_logger.info.assert_any_call('Run MCP applications in production mode...')


class TestEnvironmentOverride:
    """Tests for environment variable overrides."""

    def test_base_dir_from_env(self, runner: CliRunner) -> None:
        """Test that base dir can be set from environment."""
        with (
            patch.dict('os.environ', {'SOURCE_APPDOG': '/env/dir'}),
            patch('appdog._internal.cli.Project') as mock_project_cls,
        ):
            mock_instance = mock_project_cls.return_value
            mock_instance.paths.settings.exists.return_value = False

            result = runner.invoke(app, ['init'])

            assert result.exit_code == 0
            mock_project_cls.assert_called_once_with(project_dir=None)

    def test_base_dir_cli_overrides_env(self, runner: CliRunner) -> None:
        """Test that CLI arguments override environment variables."""
        with (
            patch.dict('os.environ', {'SOURCE_APPDOG': '/env/dir'}),
            patch('appdog._internal.cli.Project') as mock_project_cls,
        ):
            mock_instance = mock_project_cls.return_value
            mock_instance.paths.settings.exists.return_value = False

            result = runner.invoke(app, ['init', '--project', '/cli/dir'])

            assert result.exit_code == 0
            mock_project_cls.assert_called_once_with(project_dir=Path('/cli/dir'))


class TestCliShow:
    """Tests for show command."""

    def test_show_success(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test successful show of app details."""
        app_settings = AppSettings(  # type: ignore
            name='test-app',
            uri='http://example.com/api',
            base_url='http://example.com',
        )

        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_project = MagicMock(spec=Project)
            mock_project.settings = {'test-app': app_settings}
            mock_load.return_value = mock_project

            with patch('appdog._internal.cli.console.print') as mock_print:
                result = runner.invoke(
                    app,
                    [
                        'show',
                        'test-app',
                    ],
                )

                assert result.exit_code == 0
                mock_logger.info.assert_called_once_with(
                    'Showing details for application "test-app"'
                )
                mock_print.assert_called_once_with(app_settings)
                mock_load.assert_called_once_with(project_dir=None)

    def test_show_app_not_found(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test show command when app is not found."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_project = MagicMock(spec=Project)
            mock_project.settings = {}
            mock_load.return_value = mock_project

            result = runner.invoke(
                app,
                [
                    'show',
                    'test-app',
                ],
            )

            assert result.exit_code == 1
            mock_logger.info.assert_called_once_with('Showing details for application "test-app"')
            mock_logger.error.assert_called_once_with('Application "test-app" not found in project')

    def test_show_with_project_dir(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test show command with custom project directory."""
        app_settings = AppSettings(  # type: ignore
            name='test-app',
            uri='http://example.com/api',
            base_url='http://example.com',
        )

        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_project = MagicMock(spec=Project)
            mock_project.settings = {'test-app': app_settings}
            mock_load.return_value = mock_project

            with patch('appdog._internal.cli.console.print'):
                result = runner.invoke(
                    app,
                    [
                        'show',
                        'test-app',
                        '--project',
                        '/custom/dir',
                    ],
                )

                assert result.exit_code == 0
                mock_load.assert_called_once_with(project_dir=Path('/custom/dir'))

    def test_show_file_error(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test show command when file error occurs."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_load.side_effect = FileNotFoundError('Settings file not found')

            result = runner.invoke(
                app,
                [
                    'show',
                    'test-app',
                ],
            )

            assert result.exit_code == 1
            mock_logger.error.assert_called_once_with(
                'Failed to show application details: Settings file not found'
            )

    def test_show_permission_error(self, runner: CliRunner, mock_logger: MagicMock) -> None:
        """Test show command when permission error occurs."""
        with patch('appdog._internal.cli.Project.load') as mock_load:
            mock_load.side_effect = PermissionError('Permission denied')

            result = runner.invoke(
                app,
                [
                    'show',
                    'test-app',
                ],
            )

            assert result.exit_code == 1
            mock_logger.error.assert_called_once_with(
                'Failed to show application details: Permission denied'
            )
