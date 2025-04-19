import asyncio
import importlib.metadata
import logging
import sys
from pathlib import Path
from typing import Annotated, Literal

import typer
from mcp.cli import cli as mcp_cli
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from .generator import generate_mcp_file
from .logging import logger
from .managers import project_manager
from .project import Project
from .settings import AppSettings

# Initialize Rich console
console = Console()

# Initialize Typer app
app = typer.Typer(help='AppDog MCP Companion', no_args_is_help=True)

# Initialize Typer MCP app
mcp_app = typer.Typer(help='Mount applications to a MCP server or install it in a client')
app.add_typer(mcp_app, name='mcp')


def configure_logging(verbose: bool = False, debug: bool = False) -> None:
    """Configure logging with Rich handler."""
    if debug:
        root_level = logging.DEBUG
        appdog_level = logging.DEBUG
    elif verbose:
        root_level = logging.WARNING
        appdog_level = logging.DEBUG
    else:
        root_level = logging.WARNING
        appdog_level = logging.INFO

    logging.basicConfig(
        level=root_level,
        format='%(message)s',
        datefmt='[%m/%d/%y %H:%M:%S]',
        force=True,
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                markup=True,
                show_time=True,
                show_path=False,
            )
        ],
    )

    logging.getLogger('appdog').setLevel(appdog_level)


@app.command('version')
def cmd_version() -> None:
    """Show the AppDog version."""
    try:
        version = importlib.metadata.version('appdog')
        print(f'AppDog version {version}')
    except importlib.metadata.PackageNotFoundError:
        print('AppDog version unknown (package not installed)')
        sys.exit(1)


@app.callback()
def app_callback(
    verbose: Annotated[
        bool,
        typer.Option(..., '--verbose', '-v', help='Enable verbose output'),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(..., '--debug', '-d', help='Enable all debug logs, including dependencies'),
    ] = False,
) -> None:
    """Common options for all commands."""
    configure_logging(verbose, debug)


@app.command('init')
def cmd_init(
    force: Annotated[
        bool,
        typer.Option(help='Force initialization even if config already exists'),
    ] = False,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Initialize a new project."""
    logger.info(f'Initializing project in {project_dir or "current directory"}')
    try:
        project = Project(project_dir=project_dir)
        if project.paths.settings.exists() and not force:
            logger.error('Project already exists. Use `--force` to overwrite.')
            sys.exit(1)
        project.save()
        logger.info(f'Successfully initialized project in {project_dir or "current directory"}')
    except (ValueError, FileNotFoundError, PermissionError) as e:
        logger.error(f'Failed to initialize project: {e}')
        sys.exit(1)


@app.command('add')
def cmd_add(
    name: Annotated[
        str,
        typer.Argument(help='Application name'),
    ],
    uri: Annotated[
        str,
        typer.Option(..., '--uri', help='OpenAPI specification URL or file path'),
    ],
    base_url: Annotated[
        str | None,
        typer.Option(..., '--base-url', help='Base URL for API calls'),
    ] = None,
    include_methods: Annotated[
        list[str] | None,
        typer.Option(..., '--include-methods', help='Methods to include'),
    ] = None,
    exclude_methods: Annotated[
        list[str] | None,
        typer.Option(..., '--exclude-methods', help='Methods to exclude'),
    ] = None,
    include_tags: Annotated[
        list[str] | None,
        typer.Option(..., '--include-tags', help='Tags to include'),
    ] = None,
    exclude_tags: Annotated[
        list[str] | None,
        typer.Option(..., '--exclude-tags', help='Tags to exclude'),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(help='Overwrite application if it already exists with a different URI'),
    ] = False,
    frozen: Annotated[
        bool,
        typer.Option(help='Skip adding application specification in project lock file'),
    ] = False,
    upgrade: Annotated[
        bool,
        typer.Option(help='Force upgrading application specification'),
    ] = False,
    sync: Annotated[
        bool,
        typer.Option(help='Sync application specification with project registry'),
    ] = True,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Add an application to the project."""
    try:
        settings = AppSettings(
            uri=uri,
            base_url=base_url,
            include_methods=include_methods,
            exclude_methods=exclude_methods,
            include_tags=include_tags,
            exclude_tags=exclude_tags,
        )

        asyncio.run(
            _add_app_process(
                name,
                settings,
                project_dir=project_dir,
                force=force,
                frozen=frozen,
                upgrade=upgrade,
                sync=sync,
            )
        )
        logger.info(f"Successfully added project application '{name}'")
    except ValueError as e:
        logger.error(f'Failed to add project application: {e}')
        sys.exit(1)


@app.command('remove')
def cmd_remove(
    name: Annotated[
        str,
        typer.Argument(help='Application name'),
    ],
    frozen: Annotated[
        bool,
        typer.Option(help='Skip removing application specification from project lock file'),
    ] = False,
    sync: Annotated[
        bool,
        typer.Option(help='Sync application removal with project registry'),
    ] = True,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Remove an application from the project."""
    try:
        asyncio.run(
            _remove_app_process(
                name,
                project_dir=project_dir,
                frozen=frozen,
                sync=sync,
            )
        )
        logger.info(f"Successfully removed project application '{name}'")
    except (ValueError, KeyError) as e:
        logger.error(f'Failed to remove project application: {e}')
        sys.exit(1)


@app.command('list')
def cmd_list(
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """List all registered applications in the project."""
    logger.info('Listing project applications')
    try:
        project = Project.load(project_dir=project_dir)
        if not project.settings:
            logger.warning('No project applications registered')
            return
        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('Name')
        table.add_column('URI')
        for name, settings in project.settings.items():
            table.add_row(name, settings.uri)
        console.print(table)
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f'Failed to list project applications: {e}')
        sys.exit(1)


@app.command('show')
def cmd_show(
    name: Annotated[
        str,
        typer.Argument(help='Application name'),
    ],
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Show details for a specific application."""
    logger.info(f'Showing details for application "{name}"')
    try:
        project = Project.load(project_dir=project_dir)
        if name not in project.settings:
            logger.error(f'Application "{name}" not found in project')
            sys.exit(1)
        console.print(project.settings[name])
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f'Failed to show application details: {e}')
        sys.exit(1)


@app.command('lock')
def cmd_lock(
    force: Annotated[
        bool,
        typer.Option(help='Overwrite application if it exists with a different URI'),
    ] = False,
    upgrade: Annotated[
        bool,
        typer.Option(help='Overwrite application specification with a different URI'),
    ] = False,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Lock project specifications."""
    try:
        asyncio.run(
            _lock_process(
                project_dir=project_dir,
                force=force,
                upgrade=upgrade,
            )
        )
        logger.info('Successfully locked project specifications')
    except ValueError as e:
        logger.error(f'Failed to lock project specifications: {e}')
        sys.exit(1)


@app.command('sync')
def cmd_sync(
    force: Annotated[
        bool,
        typer.Option(help='Overwrite application if it exists with a different URI'),
    ] = False,
    frozen: Annotated[
        bool,
        typer.Option(help='Skip updating application specification in project lock file'),
    ] = False,
    upgrade: Annotated[
        bool,
        typer.Option(help='Force upgrading application specification'),
    ] = False,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
) -> None:
    """Sync applications with the project registry."""
    try:
        asyncio.run(
            _sync_process(
                project_dir=project_dir,
                force=force,
                frozen=frozen,
                upgrade=upgrade,
            )
        )
        logger.info('Successfully synced applications with project registry')
    except ValueError as e:
        logger.error(f'Failed to sync applications: {e}')
        sys.exit(1)


@mcp_app.command('install')
def cmd_mcp_install(
    name: Annotated[
        str,
        typer.Option(..., '--name', '-n', help='Name of the MCP server'),
    ] = 'AppDog MCP Server',
    force: Annotated[
        bool,
        typer.Option(help='Overwrite server file if it exists'),
    ] = False,
    with_editable: Annotated[
        Path | None,
        typer.Option(..., '--with-editable', '-e', help='Local package to install in edit mode'),
    ] = None,
    with_packages: Annotated[
        list[str] | None,
        typer.Option(..., '--with', help='Additional packages to install'),
    ] = None,
    env_vars: Annotated[
        list[str] | None,
        typer.Option(..., '--env-var', '-v', help='Environment variables in KEY=VALUE format'),
    ] = None,
    env_file: Annotated[
        Path | None,
        typer.Option(..., '--env-file', '-f', help='Environment file with KEY=VALUE pairs'),
    ] = None,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(..., '--output', '-o', help='Output path for MCP server file'),
    ] = None,
) -> None:
    """Install applications in MCP client."""
    logger.info('Install applications in MCP client...')
    try:
        _mcp_process(
            name=name,
            project_dir=project_dir,
            mode='install',
            force=force,
            with_editable=with_editable,
            with_packages=with_packages,
            env_vars=env_vars,
            env_file=env_file,
            output=output,
        )
    except ValueError as e:
        logger.error(f'Failed to process MCP install mode: {e}')
        sys.exit(1)


@mcp_app.command('run')
def cmd_mcp_run(
    name: Annotated[
        str,
        typer.Option(..., '--name', '-n', help='Name of the MCP server'),
    ] = 'AppDog MCP Server',
    force: Annotated[
        bool,
        typer.Option(help='Overwrite server file if it exists'),
    ] = False,
    transport: Annotated[
        str,
        typer.Option(..., '--transport', '-t', help='Transport to use for MCP run (stdio or sse)'),
    ] = 'stdio',
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(..., '--output', '-o', help='Output path for MCP server file'),
    ] = None,
) -> None:
    """Run MCP applications in production mode."""
    logger.info('Run MCP applications in production mode...')
    try:
        _mcp_process(
            name=name,
            project_dir=project_dir,
            mode='run',
            force=force,
            transport=transport,  # type: ignore
            output=output,
        )
    except ValueError as e:
        logger.error(f'Failed to process MCP run mode: {e}')
        sys.exit(1)


@mcp_app.command('dev')
def cmd_mcp_dev(
    name: Annotated[
        str,
        typer.Option(..., '--name', '-n', help='Name of the MCP server'),
    ] = 'AppDog MCP Server',
    force: Annotated[
        bool,
        typer.Option(help='Overwrite server file if it exists'),
    ] = False,
    with_editable: Annotated[
        Path | None,
        typer.Option(..., '--with-editable', '-e', help='Local package to install in edit mode'),
    ] = None,
    with_packages: Annotated[
        list[str] | None,
        typer.Option(..., '--with', help='Additional packages to install'),
    ] = None,
    project_dir: Annotated[
        Path | None,
        typer.Option(..., '--project', '-p', help='Project directory (defaults to current)'),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(..., '--output', '-o', help='Output path for MCP server file'),
    ] = None,
) -> None:
    """Run MCP applications in development mode with inspector."""
    logger.info('Run MCP applications in development mode with inspector...')
    try:
        _mcp_process(
            name=name,
            project_dir=project_dir,
            mode='dev',
            force=force,
            with_editable=with_editable,
            with_packages=with_packages,
            output=output,
        )
    except ValueError as e:
        logger.error(f'Failed to process MCP dev mode: {e}')
        sys.exit(1)


async def _add_app_process(
    name: str,
    settings: AppSettings,
    project_dir: Path | None = None,
    force: bool = False,
    frozen: bool = False,
    upgrade: bool = False,
    sync: bool = False,
) -> None:
    async with project_manager(project_dir=project_dir) as project:
        await project.add_app(
            name,
            settings,
            force=force,
            frozen=frozen,
            upgrade=upgrade,
            sync=sync,
        )


async def _remove_app_process(
    name: str,
    project_dir: Path | None = None,
    frozen: bool = False,
    sync: bool = False,
) -> None:
    async with project_manager(project_dir=project_dir) as project:
        await project.remove_app(
            name,
            frozen=frozen,
            sync=sync,
        )


async def _lock_process(
    project_dir: Path | None = None,
    force: bool = False,
    upgrade: bool = False,
) -> None:
    async with project_manager(project_dir=project_dir) as project:
        await project.lock(
            force=force,
            upgrade=upgrade,
        )


async def _sync_process(
    project_dir: Path | None = None,
    force: bool = False,
    frozen: bool = False,
    upgrade: bool = False,
) -> None:
    async with project_manager(project_dir=project_dir) as project:
        await project.sync(
            force=force,
            frozen=frozen,
            upgrade=upgrade,
        )


def _mcp_process(  # noqa: C901
    name: str,
    project_dir: Path | None = None,
    mode: Literal['install', 'run', 'dev'] = 'install',
    force: bool = False,
    with_editable: Path | None = None,
    with_packages: list[str] | None = None,
    env_vars: list[str] | None = None,
    env_file: Path | None = None,
    transport: Literal['stdio', 'sse'] | None = None,
    output: Path | None = None,
) -> None:
    # Generate MCP server file
    output = output or Path.cwd()
    if not output.is_file():
        output = output / 'appdog_mcp.py'
    if output.exists() and not force:
        logger.info(f'MCP server file generation skipped: {output} already exists')
    else:
        generate_mcp_file(
            output=output,
            project_dir=project_dir,
            server_name=name,
            overwrite=force,
        )

    # Run MCP command
    with_packages = ['appdog', *(with_packages or [])]
    env_vars = env_vars or []

    try:
        if mode == 'install':
            mcp_cli.install(
                file_spec=str(output),
                server_name=name,
                with_editable=with_editable,
                with_packages=with_packages,
                env_vars=env_vars,
                env_file=env_file,
            )
            logger.info(f'Successfully installed MCP server for {name!r}')
        elif mode == 'run':
            mcp_cli.run(
                file_spec=str(output),
                transport=transport,
            )
        elif mode == 'dev':
            mcp_cli.dev(
                file_spec=str(output),
                with_editable=with_editable,
                with_packages=with_packages,
            )
    except Exception as e:
        raise RuntimeError(f'MCP command failed: {e}') from e
