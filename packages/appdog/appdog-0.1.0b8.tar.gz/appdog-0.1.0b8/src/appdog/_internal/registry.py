import shutil
import sys
from pathlib import Path
from threading import Lock
from typing import ClassVar, NamedTuple

from typing_extensions import Self

from .generator import generate_app_files
from .logging import logger
from .specs import AppSpec, EndpointInfo, LookupConfig
from .store import Store
from .utils import get_registry_dir

REGISTRY_SPECS = 'registry.json'
"""The file name for the registry specifications."""


class RegistryPaths(NamedTuple):
    """Paths for the registry directory and files."""

    dir: Path
    """The directory for the registry specifications and applications directories."""

    specs: Path
    """The file path for the registry specifications."""


class Registry:
    """Applications registry.

    The registry class manages a collection of applications defined by their specifications. It
    provides methods to add, remove, and save applications. The registry maintains a single file:
    - `registry.json`: A JSON file that contains the registry specifications
    """

    _instance: ClassVar[Self | None] = None
    """The default applications environment registry."""

    _lock = Lock()
    """The registry thread lock."""

    def __init__(self, registry_dir: Path | str | None = None) -> None:
        self.paths = _get_registry_paths(registry_dir)
        self.specs = Store(self.paths.specs, AppSpec)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        if exc_type is None:
            self.save()

    @classmethod
    def load(cls, registry_dir: Path | str | None = None) -> Self:
        """Load the applications registry from the given directory."""
        # Load registry
        with cls._lock:
            if registry_dir is None:
                if cls._instance is not None:
                    return cls._instance
                cls._instance = cls()
                self = cls._instance
            else:
                self = cls(registry_dir)
        # Add registry directory to search paths
        registry_dir = str(self.paths.dir)
        package = sys.modules['appdog']
        if hasattr(package, '__path__'):
            if registry_dir not in package.__path__:
                logger.debug(f'Adding registry path to AppDog package: {registry_dir}')
                package.__path__.append(registry_dir)
        self.specs.read()
        return self

    def save(self, *, validate: bool = True) -> None:
        """Save the applications registry specifications file."""
        self.specs.write(validate=validate)

    def add_app(
        self,
        name: str,
        spec: AppSpec,
        *,
        force: bool = False,
        upgrade: bool = False,
    ) -> None:
        """Add an application specification to the registry.

        Args:
            name: The name of the application
            spec: The application specification
            force: Whether to add application even if it already exists with a different URI
            upgrade: Whether to force upgrade application specification
        """
        logger.debug(f'Adding {name!r} application to registry...')
        # Handle existing application
        if name in self.specs:
            current_spec = self.specs[name]
            if current_spec.uri != spec.uri:
                if not force:
                    raise ValueError(f'Registry application {name!r} exists with different URI')
                logger.warning(f'Upgrading registry application {name!r} URI to {spec.uri}')
            elif upgrade or current_spec.hash != spec.hash:
                logger.debug(f'Upgrading registry application {name!r}')
            else:
                logger.debug(f'Registry application {name!r} requirements already satisfied')
                return
        # Generate application directory
        generate_app_files(name, spec, self.paths.dir, overwrite=True)
        # Add application specification
        self.specs[name] = spec

    def remove_app(self, name: str) -> None:
        """Remove an application from the registry."""
        logger.debug(f'Removing {name!r} application from registry...')
        if name not in self.specs:
            logger.warning(f'Registry application {name!r} is not registered')
            return
        # Remove application directory
        shutil.rmtree(self.paths.dir / name, ignore_errors=True)
        # Remove application specification
        del self.specs[name]

    def lookup(self, **config: LookupConfig | bool) -> dict[str, list[EndpointInfo]]:
        """Lookup endpoints with the given application lookup configurations.

        Args:
            **config: Application lookup configuration or boolean to include all applications
                endpoints. When provided, only applications matching the filters will be included.
                Otherwise, all applications endpoints will be included.

        Returns:
            Dictionary mapping application names to lists of endpoint information.
        """
        endpoints = {}
        for name, spec in self.specs.items():
            # Resolve lookup configuration
            if config and name not in config:
                continue
            lookup_config = config.get(name)
            if lookup_config is False:
                continue
            elif lookup_config is True or lookup_config is None:
                lookup_config = {}
            # Apply lookup configuration
            endpoints[name] = spec.lookup(**lookup_config)
        return endpoints


def _get_registry_paths(registry_dir: Path | str | None = None) -> RegistryPaths:
    """Get the environment registry directory and file paths."""
    registry_dir = Path(registry_dir) if registry_dir else get_registry_dir()
    return RegistryPaths(
        dir=registry_dir,
        specs=registry_dir / REGISTRY_SPECS,
    )
