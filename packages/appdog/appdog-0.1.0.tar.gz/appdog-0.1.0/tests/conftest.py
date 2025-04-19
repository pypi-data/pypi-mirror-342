from typing import Any

import pytest


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Fixture providing sample data dictionaries for testing."""
    return {
        'simple': {'key': 'value'},
        'nested': {'outer': {'inner': 'value'}, 'list': [1, 2, 3]},
        'ordered': {'a': 1, 'b': 2, 'c': 3},
        'unordered': {'c': 3, 'a': 1, 'b': 2},
    }


class AsyncNoWarningMock:
    """
    A mock for async functions that doesn't produce warnings.

    This is a simple callable that returns a value immediately instead of a coroutine,
    preventing the "coroutine was never awaited" warnings.
    """

    def __init__(self, return_value: Any = None) -> None:
        self.return_value = return_value
        self.call_count = 0
        self.call_args: Any | None = None
        self.call_args_list: list[Any] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Record the call and return the configured return value."""
        self.call_count += 1
        self.call_args = (args, kwargs)
        self.call_args_list.append((args, kwargs))
        return self

    def __await__(self) -> Any:
        """Make this mock awaitable."""

        async def _awaitable() -> Any:
            return self.return_value

        return _awaitable().__await__()

    def assert_called_once(self) -> None:
        """Assert the mock was called exactly once."""
        if self.call_count != 1:
            raise AssertionError(f'Expected 1 call, got {self.call_count}')
