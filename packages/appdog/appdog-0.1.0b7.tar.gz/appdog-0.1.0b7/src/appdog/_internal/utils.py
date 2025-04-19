import datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any


def compute_hash(data: dict[str, Any]) -> str:
    """Compute the hash of the given dictionary."""
    data_json = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_json.encode()).hexdigest()


def get_project_dir() -> Path:
    """Get the path to the project directory."""
    project_dir = os.environ.get('APPDOG_PROJECT')
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def get_registry_dir() -> Path:
    """Get the path to the registry directory."""
    registry_dir = os.environ.get('APPDOG_REGISTRY')
    if registry_dir:
        return Path(registry_dir)
    return get_source_dir()


def get_source_dir() -> Path:
    """Get the path to the applications source directory."""
    return Path(__file__).parent.parent


def get_timestamp() -> str:
    """Get the current timestamp."""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
