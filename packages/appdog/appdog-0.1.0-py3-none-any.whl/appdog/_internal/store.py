import json
import typing
from collections.abc import (
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    MutableMapping,
    ValuesView,
)
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Protocol, TypeVar

import yaml
from pydantic import Field, RootModel, ValidationError, model_validator
from typing_extensions import Self
from yaml import YAMLError

_T = TypeVar('_T')
_T_co = TypeVar('_T_co')


@typing.runtime_checkable
class SupportsKeysAndGetItem(Protocol):
    def keys(self) -> Iterable[str]: ...
    def __getitem__(self, key: str, /) -> Any: ...


class StoreData(RootModel[dict[str, _T]]):
    """A generic dictionary root model to store data."""

    root: dict[str, _T] = Field(default_factory=dict)

    @model_validator(mode='after')
    def model_validate_keys(self) -> Self:
        for key in self.root.keys():
            if not key or key.startswith('_'):
                raise ValueError('Key must not be empty or start with underscore')
            if not all(char.islower() or char.isdigit() or char == '_' for char in key):
                raise ValueError('Key must be snake case (lowercase with underscores)')
        return self


class Store(MutableMapping[str, _T]):
    """A generic store to persist data to a local file."""

    def __init__(
        self,
        __file_path: Path | str,
        __type: type[_T] = Any,  # type: ignore
        **data: _T,
    ) -> None:
        self.file_path = Path(__file_path).resolve()
        if self.file_path.suffix in ('.json', '.lock'):
            self.format = 'json'
        elif self.file_path.suffix in ('.yaml', '.yml'):
            self.format = 'yaml'
        else:
            raise ValueError('File path must target a JSON or YAML file')
        self.data = StoreData[__type](data)  # type: ignore

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        if exc_type is None:
            self.write()

    @classmethod
    def load(cls, file_path: Path | str, *, raise_missing: bool = False) -> Self:
        """Load the store from the given file path."""
        self = cls(file_path)
        self.read(raise_missing=raise_missing)
        return self

    def read(self, *, raise_missing: bool = False) -> None:
        """Read the store from the given file path."""
        if not self.file_path.exists():
            if not raise_missing:
                return
            raise OSError(f'File does not exist: {self.file_path}')
        if self.format == 'json':
            self._read_json()
        elif self.format == 'yaml':
            self._read_yaml()

    def write(self, *, validate: bool = True) -> None:
        """Write the store to the given file path."""
        if self.format == 'json':
            self._write_json()
        elif self.format == 'yaml':
            self._write_yaml()

    def validate(self, data: Any | None = None) -> None:
        """Validate the store data or the given data."""
        if data is None:
            data = self.data.root
        self.data.__pydantic_validator__.validate_python(data, self_instance=self.data)

    def _read_json(self) -> None:
        try:
            with open(self.file_path) as f:
                data = json.load(f)
            self.validate(data)
        except JSONDecodeError as e:
            raise OSError(f'Failed to parse file: {self.file_path}') from e
        except ValidationError as e:
            raise OSError(f'Failed to validate file: {self.file_path}') from e
        except Exception as e:
            raise OSError(f'Failed to read file: {self.file_path}') from e

    def _read_yaml(self) -> None:
        try:
            with open(self.file_path) as f:
                data = yaml.safe_load(f)
            self.validate(data)
        except YAMLError as e:
            raise OSError(f'Failed to parse file: {self.file_path}') from e
        except ValidationError as e:
            raise OSError(f'Failed to validate file: {self.file_path}') from e
        except Exception as e:
            raise OSError(f'Failed to read file: {self.file_path}') from e

    def _write_json(self) -> None:
        try:
            self.validate()
            data = self.data.model_dump(mode='json', exclude_unset=True)
            data = json.dumps(data) or ''
            with open(self.file_path, 'w') as f:
                f.write(data)
        except Exception as e:
            raise OSError(f'Failed to write file: {self.file_path}') from e

    def _write_yaml(self) -> None:
        try:
            self.validate()
            data = self.data.model_dump(mode='json', exclude_unset=True)
            data = yaml.dump(data) or ''
            with open(self.file_path, 'w') as f:
                f.write(data)
        except Exception as e:
            raise OSError(f'Failed to write file: {self.file_path}') from e

    @typing.overload
    def get(self, key: str, /) -> _T | None: ...

    @typing.overload
    def get(self, key: str, /, default: _T | _T_co) -> _T | _T_co: ...

    def get(self, key: str, /, default: _T | _T_co | None = None) -> _T | _T_co | None:
        return self.data.root.get(key, default)

    def keys(self) -> KeysView[str]:
        return KeysView(self.data.root)

    def values(self) -> ValuesView[_T]:
        return ValuesView(self.data.root)

    def items(self) -> ItemsView[str, _T]:
        return ItemsView(self.data.root)

    def clear(self) -> None:
        self.data.root.clear()

    @typing.overload
    def pop(self, key: str, /) -> _T: ...

    @typing.overload
    def pop(self, key: str, /, default: _T) -> _T: ...

    @typing.overload
    def pop(self, key: str, /, default: _T_co) -> _T | _T_co: ...

    def pop(self, key: str, /, default: Any = ...) -> Any:
        if default is ...:
            return self.data.root.pop(key)
        return self.data.root.pop(key, default)

    def popitem(self) -> tuple[str, _T]:
        return self.data.root.popitem()

    @typing.overload
    def setdefault(self, key: str, default: None = None, /) -> _T | None: ...

    @typing.overload
    def setdefault(self, key: str, default: _T, /) -> _T: ...

    def setdefault(self, key: str, default: Any = None, /) -> Any:
        return self.data.root.setdefault(key, default)

    @typing.overload
    def update(self, *args: SupportsKeysAndGetItem, **kwargs: _T) -> None: ...

    @typing.overload
    def update(self, *args: Iterable[tuple[str, _T]], **kwargs: _T) -> None: ...

    def update(self, *args: Any, **kwargs: Any) -> None:
        for arg in args:
            if isinstance(arg, SupportsKeysAndGetItem):
                for key in arg.keys():
                    self.data.root[key] = arg[key]
            else:
                for key, value in arg:
                    self.data.root[key] = value
        self.data.root.update(**kwargs)

    def __contains__(self, key: object) -> bool:
        return key in self.data.root

    def __iter__(self) -> Iterator[str]:  # type: ignore
        yield from self.data.root

    def __reversed__(self) -> Iterator[str]:
        yield from reversed(self.data.root)

    def __len__(self) -> int:
        return len(self.data.root)

    def __getitem__(self, key: str) -> _T:
        return self.data.root[key]

    def __setitem__(self, key: str, value: _T) -> None:
        self.data.root[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data.root[key]
