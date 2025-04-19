from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from .project import Project
from .registry import Registry


@asynccontextmanager
async def project_manager(
    project_dir: Path | str | None = None,
    registry_dir: Path | str | None = None,
) -> AsyncGenerator[Project, None]:
    """Context manager for project that automatically saves when exiting.

    Args:
        project_dir: Path to project directory (default: auto-detect)
        registry_dir: Path to registry directory (default: auto-detect)
    """
    async with Project.load(project_dir, registry_dir) as context:
        yield context


@asynccontextmanager
async def registry_manager(
    registry_dir: Path | str | None = None,
) -> AsyncGenerator[Registry, None]:
    """Context manager for registry that automatically saves when exiting.

    Args:
        registry_dir: Path to registry directory (default: auto-detect)
    """
    async with Registry.load(registry_dir) as context:
        yield context
