from pathlib import Path
from typing import NamedTuple

from mcp.server.fastmcp import FastMCP
from typing_extensions import Self

from .logging import logger
from .mcp import mount_to_fastmcp
from .registry import Registry
from .settings import AppSettings
from .specs import AppSpec, EndpointInfo, LookupConfig
from .store import Store
from .utils import get_project_dir

PROJECT_LOCK = 'apps.lock'
"""The file name for the project locked specifications."""

PROJECT_SETTINGS = 'apps.yaml'
"""The file name for the project settings."""


class ProjectPaths(NamedTuple):
    """Paths for the project directory and files."""

    dir: Path
    """The directory for the project settings and locked specifications files."""

    settings: Path
    """The file path for the project settings."""

    specs: Path
    """The file path for the project locked specifications."""


class Project:
    """Applications project.

    The project class manages a collection of applications defined by their settings and
    specifications. It provides methods to add, remove, and sync applications with a registry. The
    project maintains two primary files:
    - `apps.yaml`: A settings file that contains application settings in YAML format
    - `apps.lock`: A lock file that contains locked application specifications in JSON format
    """

    def __init__(
        self,
        project_dir: Path | str | None = None,
        registry_dir: Path | str | None = None,
    ) -> None:
        self.paths = _get_project_paths(project_dir)
        self.registry = Registry.load(registry_dir)
        self.specs = Store(self.paths.specs, AppSpec)
        self.settings = Store(self.paths.settings, AppSettings)

    async def __aenter__(self) -> Self:
        await self.registry.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        await self.registry.__aexit__(exc_type, exc_val, exc_tb)
        if exc_type is None:
            self.save()

    @classmethod
    def load(
        cls,
        project_dir: Path | str | None = None,
        registry_dir: Path | str | None = None,
    ) -> Self:
        """Load the applications project from the given project and registry directories."""
        self = cls(project_dir, registry_dir)
        self.settings.read()
        self.specs.read()
        return self

    def save(self) -> None:
        """Save the applications project settings and locked specifications files."""
        self.settings.write()
        self.specs.write()

    async def add_app(
        self,
        name: str,
        settings: AppSettings,
        *,
        force: bool = False,
        frozen: bool = False,
        upgrade: bool = False,
        sync: bool = False,
    ) -> None:
        """Add an application to the project.

        Args:
            name: The name of the application
            settings: The application settings
            force: Whether to overwrite application if it already exists with a different URI
            frozen: Whether to skip adding application specification in the project lock file
            upgrade: Whether to force upgrading application specification
            sync: Whether to sync application specification with the project registry
        """
        logger.info(f'Adding {name!r} application to project...')
        # Handle existing application
        if name in self.settings:
            current_settings = self.settings[name]
            if settings.uri != current_settings.uri:
                if not force:
                    raise ValueError(f'Project application {name!r} exists with different URI')
                logger.warning(f'Upgrading project application {name!r} URI to {settings.uri}')
        # Add application specification
        if not frozen:
            current_spec = self.specs.get(name)
            if upgrade or current_spec is None or current_spec.uri != settings.uri:
                try:
                    self.specs[name] = await AppSpec.fetch(settings.uri)
                except Exception as e:
                    raise ValueError(f'Failed to fetch specification for {name!r}') from e
            if sync:
                self.registry.add_app(
                    name,
                    self.specs[name],
                    force=force,
                    upgrade=upgrade,
                )
        # Add application settings
        self.settings[name] = settings

    async def remove_app(
        self,
        name: str,
        *,
        frozen: bool = False,
        sync: bool = False,
    ) -> None:
        """Remove an application from the project.

        Args:
            name: The name of the application
            frozen: Whether to skip removing application specification from the project lock file
            sync: Whether to sync application specification with the project registry
        """
        logger.info(f'Removing {name!r} application from project...')
        # Handle non-existing application
        if name not in self.settings:
            logger.warning(f'Project application {name!r} is not registered')
            return
        # Remove application specification
        if not frozen:
            if sync:
                try:
                    self.registry.remove_app(name)
                except Exception as e:  # noqa: BLE001
                    logger.warning(f'Failed to remove application {name!r} from registry: {e}')
            if name in self.specs:
                del self.specs[name]
        # Remove application settings
        del self.settings[name]

    async def lock(
        self,
        *,
        force: bool = False,
        upgrade: bool = False,
    ) -> None:
        """Lock project specifications.

        Args:
            force: Whether to overwrite application if it already exists with a different URI
            upgrade: Whether to force upgrading application specification
        """
        logger.info('Locking project specifications...')
        specs = {name: spec for name, spec in self.specs.items() if name in self.settings}
        for name, settings in self.settings.items():
            if name in specs:
                spec = specs[name]
                if spec.uri != settings.uri:
                    if not force:
                        raise ValueError(f'Project application {name!r} exists with different URI')
                    logger.warning(f'Upgrading project application {name!r} URI to {settings.uri}')
                elif upgrade:
                    logger.info(f'Upgrading project application {name!r}')
                else:
                    logger.info(f'Project application {name!r} requirements already satisfied')
                    continue
            try:
                specs[name] = await AppSpec.fetch(settings.uri)
            except Exception as e:
                raise ValueError(f'Failed to fetch specification for {name!r}') from e
        self.specs.clear()
        self.specs.update(specs)

    async def sync(
        self,
        *,
        force: bool = False,
        frozen: bool = False,
        upgrade: bool = False,
    ) -> None:
        """Sync applications with the project registry.

        Args:
            force: Whether to overwrite application if it already exists with a different URI
            frozen: Whether to skip updating application specification in the project lock file
            upgrade: Whether to force upgrading application specification
        """
        logger.info('Syncing applications with project registry...')
        # Lock project specifications
        if not frozen:
            try:
                await self.lock(force=force, upgrade=upgrade)
            except Exception as e:
                raise ValueError('Failed to lock project specifications') from e
        # Sync applications with the project registry
        for name, spec in self.specs.items():
            try:
                self.registry.add_app(
                    name,
                    spec,
                    force=force,
                    upgrade=upgrade,
                )
            except Exception as e:  # noqa: BLE001
                raise ValueError(f'Failed to sync application {name!r}: {e}') from e

    def lookup(self, **config: LookupConfig | bool | None) -> dict[str, list[EndpointInfo]]:
        """Lookup endpoints with the given application lookup configurations.

        Args:
            **config: Application lookup configuration or boolean to include all applications
                endpoints. When provided, only applications matching the filters will be included.
                Otherwise, all applications endpoints will be included.

        Returns:
            Dictionary mapping application names to lists of endpoint information.
        """
        endpoints = {}
        for name, settings in self.settings.items():
            spec = self.specs[name]
            if spec is None:
                logger.warning(f'Project application {name!r} specification is missing')
                continue
            # Resolve lookup configuration
            if config and name not in config:
                continue
            lookup_config = config.get(name)
            if lookup_config is None:
                lookup_config = settings.get_lookup_config()
            elif lookup_config is False:
                continue
            elif lookup_config is True:
                lookup_config = {}
            # Apply lookup configuration
            endpoints[name] = spec.lookup(**lookup_config)
        return endpoints

    def mount(self, __server: FastMCP, **config: LookupConfig | bool | None) -> None:
        """Mount the project to a FastMCP server with the given lookup configuration.

        Args:
            server: The FastMCP server to mount the project to
            **config: Application lookup configuration or boolean to include all applications
                endpoints. When provided, only applications matching the filters will be included.
                Otherwise, all applications endpoints will be included.
        """
        endpoints = self.lookup(**config)
        mount_to_fastmcp(__server, endpoints)


def _get_project_paths(project_dir: Path | str | None = None) -> ProjectPaths:
    """Get the project directory and file paths."""
    project_dir = Path(project_dir) if project_dir else get_project_dir()
    return ProjectPaths(
        dir=project_dir,
        settings=project_dir / PROJECT_SETTINGS,
        specs=project_dir / PROJECT_LOCK,
    )
