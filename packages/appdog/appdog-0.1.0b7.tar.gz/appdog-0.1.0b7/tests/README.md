# Testing

This directory contains tests for the source_appdog project. The tests are organized by module and use pytest as the testing framework.

## Test Organization

- **`test_case.py`**: Tests for case conversion utilities
- **`test_clients.py`**: Tests for API client functionality
- **`test_mcp.py`**: Tests for MCP (Message Control Protocol) integration
- **`test_project.py`**: Tests for Project management functionality
- **`test_registry.py`**: Tests for application registry
- **`test_settings.py`**: Tests for settings management
- **`test_specs.py`**: Tests for application specifications
- **`test_store.py`**: Tests for data storage

## Running Tests

### Using pytest directly

Run all tests:
```bash
python -m pytest
```

Run tests with verbose output:
```bash
python -m pytest -v
```

Run specific test files:
```bash
python -m pytest tests/test_mcp.py tests/test_project.py
```

Run specific test cases:
```bash
python -m pytest tests/test_mcp.py::TestMCPResolver
```

Run specific test methods:
```bash
python -m pytest tests/test_project.py::TestProject::test_mount_with_no_filters
```

### Using Hatch Scripts

This project uses [Hatch](https://hatch.pypa.io/latest/) for managing development tasks. The following scripts are defined in `pyproject.toml`:

#### Test Commands

```bash
# Run all tests
hatch run test:py

# Run tests with coverage report
hatch run test:cov

# View coverage report in browser
hatch run test:html

# Run specific tests with pytest arguments
hatch run test:py -- tests/test_mcp.py -v
```

#### Lint and Formatting Commands

While there are no explicit lint scripts defined in pyproject.toml, you can run standard linting commands as follows:

```bash
# Run ruff linter
ruff check .

# Apply ruff fixes automatically
ruff check --fix .

# Format code with ruff
ruff format .
```

#### Type Checking Commands

```bash
# Run mypy type checking
mypy src tests
```

## Test Fixtures

Common test fixtures are available in the test files to simplify test setup:

- Mock FastMCP servers
- Sample endpoint information
- Test functions
- Project fixtures with mock registries

## Best Practices

1. Each test should focus on a single piece of functionality
2. Use appropriate mocking to isolate the code being tested
3. Avoid blind exception catching
4. Tests should be deterministic and not depend on external services
