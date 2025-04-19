import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from appdog._internal.store import Store, StoreData


class TestStoreData:
    def test_valid_keys(self) -> None:
        """Test that valid keys are accepted."""
        data = {
            'valid_key': 1,
            'another_valid_key': 2,
            'numeric123': 3,
        }
        store_data = StoreData(data)
        assert store_data.root == data

    def test_empty_key(self) -> None:
        """Test that empty keys are rejected."""
        data = {'': 1}
        with pytest.raises(ValueError, match='Key must not be empty'):
            StoreData(data)

    def test_underscore_prefix_key(self) -> None:
        """Test that keys starting with underscore are rejected."""
        data = {'_invalid_key': 1}
        with pytest.raises(ValueError, match='Key must not be empty or start with underscore'):
            StoreData(data)

    def test_non_snake_case_key(self) -> None:
        """Test that non-snake-case keys are rejected."""
        data = {'InvalidKey': 1}
        with pytest.raises(ValueError, match='Key must be snake case'):
            StoreData(data)


class TestStore:
    @pytest.fixture
    def temp_json_file(self, tmp_path: Path) -> Path:
        """Fixture providing a temporary JSON file path."""
        return tmp_path / 'test_store.json'

    @pytest.fixture
    def temp_yaml_file(self, tmp_path: Path) -> Path:
        """Fixture providing a temporary YAML file path."""
        return tmp_path / 'test_store.yaml'

    @pytest.fixture
    def sample_data(self) -> dict[str, Any]:
        """Fixture providing sample data for testing."""
        return {
            'test_key': 'test_value',
            'another_key': 42,
            'nested_key': {'inner_key': 'inner_value'},
        }

    def test_init_with_json_path(self, temp_json_file: Path) -> None:
        """Test initializing with a JSON file path."""
        store_obj = Store[Any](temp_json_file)
        assert store_obj.file_path == temp_json_file
        assert store_obj.format == 'json'
        assert store_obj.data.root == {}

    def test_init_with_yaml_path(self, temp_yaml_file: Path) -> None:
        """Test initializing with a YAML file path."""
        store_obj = Store[Any](temp_yaml_file)
        assert store_obj.file_path == temp_yaml_file
        assert store_obj.format == 'yaml'
        assert store_obj.data.root == {}

    def test_init_with_invalid_format(self, tmp_path: Path) -> None:
        """Test initializing with an invalid file format."""
        invalid_file = tmp_path / 'invalid.txt'
        with pytest.raises(ValueError, match='File path must target a JSON or YAML file'):
            Store(invalid_file)

    def test_init_with_data(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test initializing with data."""
        store_obj = Store[Any](temp_json_file, **sample_data)
        assert store_obj.data.root == sample_data

    def test_context_manager(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test using the store as a context manager."""
        with Store(temp_json_file, **sample_data) as store_obj:
            store_obj['new_key'] = 'new_value'

        # Verify file was written
        assert temp_json_file.exists()

        # Read the file to verify content
        with open(temp_json_file) as f:
            saved_data = json.load(f)

        expected = sample_data.copy()
        expected['new_key'] = 'new_value'
        assert saved_data == expected

    def test_load_existing_json(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test loading from an existing JSON file."""
        # Create a file with sample data
        with open(temp_json_file, 'w') as f:
            json.dump(sample_data, f)

        # Load the store from the file
        store_obj = Store[Any].load(temp_json_file)
        assert store_obj.data.root == sample_data

    def test_load_existing_yaml(self, temp_yaml_file: Path, sample_data: dict[str, Any]) -> None:
        """Test loading from an existing YAML file."""
        # Create a file with sample data
        with open(temp_yaml_file, 'w') as f:
            yaml.dump(sample_data, f)

        # Load the store from the file
        store_obj = Store[Any].load(temp_yaml_file)
        assert store_obj.data.root == sample_data

    def test_load_missing_file(self, temp_json_file: Path) -> None:
        """Test loading from a non-existent file."""
        # Without raise_missing
        store_obj = Store[Any].load(temp_json_file)
        assert store_obj.data.root == {}

        # With raise_missing
        with pytest.raises(OSError, match='File does not exist'):
            Store[Any].load(temp_json_file, raise_missing=True)

    def test_read_invalid_json(self, temp_json_file: Path) -> None:
        """Test reading from an invalid JSON file."""
        # Create an invalid JSON file
        with open(temp_json_file, 'w') as f:
            f.write('{"invalid": json')

        store_obj = Store[Any](temp_json_file)
        with pytest.raises(OSError, match='Failed to parse file'):
            store_obj.read()

    def test_read_invalid_yaml(self, temp_yaml_file: Path) -> None:
        """Test reading from an invalid YAML file."""
        # Create an invalid YAML file
        with open(temp_yaml_file, 'w') as f:
            f.write('invalid: yaml:')

        store_obj = Store[Any](temp_yaml_file)
        with pytest.raises(OSError, match='Failed to parse file'):
            store_obj.read()

    def test_write_json(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test writing to a JSON file."""
        store_obj = Store[Any](temp_json_file, **sample_data)
        store_obj.write()

        # Verify file exists
        assert temp_json_file.exists()

        # Read the file to verify content
        with open(temp_json_file) as f:
            saved_data = json.load(f)

        assert saved_data == sample_data

    def test_write_yaml(self, temp_yaml_file: Path, sample_data: dict[str, Any]) -> None:
        """Test writing to a YAML file."""
        store_obj = Store[Any](temp_yaml_file, **sample_data)
        store_obj.write()

        # Verify file exists
        assert temp_yaml_file.exists()

        # Read the file to verify content
        with open(temp_yaml_file) as f:
            saved_data = yaml.safe_load(f)

        assert saved_data == sample_data

    def test_validation_failure(self, temp_json_file: Path) -> None:
        """Test validation failure on invalid data."""
        # Create a store with valid data
        store_obj = Store[Any](temp_json_file)

        # Try to validate invalid data (keys with uppercase)
        invalid_data = {'InvalidKey': 'value'}
        with pytest.raises(ValidationError):
            store_obj.validate(invalid_data)

    def test_dict_like_methods(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test dictionary-like methods of the Store class."""
        store_obj = Store[Any](temp_json_file, **sample_data)

        # Test __getitem__
        assert store_obj['test_key'] == 'test_value'

        # Test __setitem__
        store_obj['new_key'] = 'new_value'
        assert store_obj['new_key'] == 'new_value'

        # Test __delitem__
        del store_obj['test_key']
        assert 'test_key' not in store_obj

        # Test __contains__
        assert 'another_key' in store_obj
        assert 'nonexistent_key' not in store_obj

        # Test __len__
        assert len(store_obj) == 3  # another_key, nested_key, new_key

        # Test get
        assert store_obj.get('another_key') == 42
        assert store_obj.get('nonexistent_key') is None
        assert store_obj.get('nonexistent_key', 'default') == 'default'

        # Test keys, values, items
        assert set(store_obj.keys()) == {'another_key', 'nested_key', 'new_key'}

        # Test values - can't use set for dictionaries (unhashable)
        values = list(store_obj.values())
        assert len(values) == 3
        assert 42 in values
        assert 'new_value' in values
        nested_dict = {'inner_key': 'inner_value'}
        assert any(v == nested_dict for v in values)

        # Test items - can't use set for items with dict values
        items = list(store_obj.items())
        assert len(items) == 3
        assert ('another_key', 42) in items
        assert ('new_key', 'new_value') in items
        assert ('nested_key', nested_dict) in items

        # Test __iter__
        assert set(iter(store_obj)) == {'another_key', 'nested_key', 'new_key'}

        # Test clear
        store_obj.clear()
        assert len(store_obj) == 0

    def test_update_method(self, temp_json_file: Path) -> None:
        """Test the update method."""
        store_obj = Store[Any](temp_json_file)

        # Update with dict
        store_obj.update({'key1': 'value1', 'key2': 'value2'})
        assert store_obj['key1'] == 'value1'
        assert store_obj['key2'] == 'value2'

        # Update with keyword arguments
        store_obj.update(key3='value3', key4='value4')
        assert store_obj['key3'] == 'value3'
        assert store_obj['key4'] == 'value4'

        # Update with iterable of pairs
        store_obj.update([('key5', 'value5'), ('key6', 'value6')])
        assert store_obj['key5'] == 'value5'
        assert store_obj['key6'] == 'value6'

    def test_pop_method(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test the pop method."""
        store_obj = Store[Any](temp_json_file, **sample_data)

        # Pop existing key
        value = store_obj.pop('test_key')
        assert value == 'test_value'
        assert 'test_key' not in store_obj

        # Pop with default for nonexistent key
        value = store_obj.pop('nonexistent_key', 'default')
        assert value == 'default'

        # Pop nonexistent key without default
        with pytest.raises(KeyError):
            store_obj.pop('nonexistent_key')

    def test_popitem_method(self, temp_json_file: Path, sample_data: dict[str, Any]) -> None:
        """Test the popitem method."""
        store_obj = Store(temp_json_file, **sample_data)

        # Pop an item
        key, value = store_obj.popitem()
        assert key in sample_data
        assert value == sample_data[key]
        assert key not in store_obj

        # Clear and test popitem on empty store
        store_obj.clear()
        with pytest.raises(KeyError):
            store_obj.popitem()

    def test_setdefault_method(self, temp_json_file: Path) -> None:
        """Test the setdefault method."""
        store_obj = Store[Any](temp_json_file)

        # Set default for nonexistent key
        value = store_obj.setdefault('key1', 'default1')
        assert value == 'default1'
        assert store_obj['key1'] == 'default1'

        # Set default for existing key
        value = store_obj.setdefault('key1', 'default2')
        assert value == 'default1'  # Original value is returned
        assert store_obj['key1'] == 'default1'  # Value is unchanged
