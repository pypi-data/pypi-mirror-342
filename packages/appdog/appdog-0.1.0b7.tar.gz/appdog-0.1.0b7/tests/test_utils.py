import datetime
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from appdog._internal.utils import compute_hash, get_registry_dir, get_timestamp


class TestComputeHash:
    def test_compute_hash_with_simple_dict(self, sample_data: dict[str, Any]) -> None:
        """Test compute_hash with a simple dictionary."""
        test_dict = sample_data['simple']
        expected = hashlib.sha256(json.dumps(test_dict, sort_keys=True).encode()).hexdigest()
        assert compute_hash(test_dict) == expected

    def test_compute_hash_with_nested_dict(self, sample_data: dict[str, Any]) -> None:
        """Test compute_hash with a nested dictionary."""
        test_dict = sample_data['nested']
        expected = hashlib.sha256(json.dumps(test_dict, sort_keys=True).encode()).hexdigest()
        assert compute_hash(test_dict) == expected

    def test_compute_hash_deterministic(self, sample_data: dict[str, Any]) -> None:
        """Test that compute_hash produces the same hash for the same data regardless of order."""
        ordered_dict = sample_data['ordered']
        unordered_dict = sample_data['unordered']
        assert compute_hash(ordered_dict) == compute_hash(unordered_dict)

    def test_compute_hash_different_for_different_data(self) -> None:
        """Test that compute_hash produces different hashes for different data."""
        dict1 = {'key': 'value1'}
        dict2 = {'key': 'value2'}
        assert compute_hash(dict1) != compute_hash(dict2)


class TestGetSourceDir:
    def test_get_registry_dir_returns_path(self) -> None:
        """Test that get_registry_dir returns a Path object."""
        registry_dir = get_registry_dir()
        assert isinstance(registry_dir, Path)

    def test_get_registry_dir_points_to_src(self) -> None:
        """Test that get_registry_dir points to the src directory."""
        registry_dir = get_registry_dir()
        assert registry_dir.name == 'appdog'
        assert registry_dir.is_dir()


class TestGetTimestamp:
    def test_get_timestamp_returns_string(self) -> None:
        """Test that get_timestamp returns a string."""
        timestamp = get_timestamp()
        assert isinstance(timestamp, str)

    def test_get_timestamp_is_parsable(self) -> None:
        """Test that get_timestamp returns a parsable datetime string."""
        timestamp = get_timestamp()
        try:
            datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            parsable = True
        except ValueError:
            parsable = False
        assert parsable

    def test_get_timestamp_format_matches_expected_pattern(self) -> None:
        """Test that get_timestamp matches the expected pattern."""
        timestamp = get_timestamp()
        assert len(timestamp) == 19  # YYYY-MM-DD HH:MM:SS (19 characters)

        # Check format with regex pattern
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        assert re.match(pattern, timestamp) is not None
