# Contributing to AppDog

Thank you for considering contributing to AppDog! This document outlines the process for contributing to the project and how to get started.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct, which is to treat all contributors with respect and foster an inclusive environment.

## Getting Started

### Development Environment

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/yourusername/appdog.git
   cd appdog
   ```

2. Set up the development environment with uv:
   ```bash
   # Install uv if you don't have it
   curl -sSf https://install.python-poetry.org | python3 -

   # Create and activate a virtual environment
   uv venv

   # Install dependencies including development dependencies
   uv pip install -e ".[dev,test]"
   ```

3. Verify the setup by running tests:
   ```bash
   python -m pytest
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names that reflect the changes you're making:
- `feature/name-of-feature`: For new features
- `fix/issue-description`: For bug fixes
- `refactor/component-name`: For code refactoring
- `docs/item-documented`: For documentation changes

### Commit Messages

Write clear, concise commit messages that explain what you changed and why. Format your commit messages like this:
```
category: concise description of changes

Longer description explaining the rationale if needed.
```

Categories include: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

1. Before submitting a pull request, make sure that:
   - Your code follows the style guidelines (see below)
   - All tests pass
   - You've added tests for new functionality
   - You've updated documentation as necessary

2. Open a pull request with a clear title and description. Include:
   - What the change does
   - Why it's needed
   - Any relevant issue numbers (e.g., "Fixes #123")

## Coding Standards

### Style Guidelines

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting. Configuration is in `pyproject.toml`. Run the linter before committing:

```bash
ruff check .
ruff format .
```

### Type Checking

This project uses [mypy](https://github.com/python/mypy) for static type checking:

```bash
mypy src tests
```

### Testing

Tests are written using [pytest](https://pytest.org/). All new code should be accompanied by tests. Run tests with:

```bash
pytest
# Or for coverage report
python -m pytest --cov=src --cov-report=term --cov-report=html
```

## Documentation

Documentation should be updated along with code changes. Comment your code where it's not immediately obvious what it does, especially for complex functions and methods.

For public API, ensure:
- Functions and classes have docstrings
- Function parameters and return types are documented
- Examples are included for common use cases

## Release Process

The maintainers will handle releases according to the following process:

1. Update version in `src/appdog/__init__.py`
2. Update CHANGELOG.md
3. Create a tagged release
4. Build and publish to PyPI

## Getting Help

If you need help with your contribution:

- Open an issue for discussion
- Ask questions in the repository's discussions section
- Mention specific maintainers in your PR if you need guidance

## Project Structure

Familiarize yourself with the project structure before contributing:

```
src/
└── appdog/                  # AppDog package
    ├── __init__.py        # Package initialization
    ├── __main__.py        # CLI entrypoint
    ├── _internal/         # Internal implementation (not exposed)
    │   ├── templates/     # Jinja templates for code generation
    │   ├── case.py        # Case conversion utilities
    │   ├── cli.py         # CLI implementation
    │   ├── clients.py     # Base client classes
    │   ├── errors.py      # Custom exceptions
    │   ├── generator.py   # Client generation
    │   ├── logging.py     # Logging configuration
    │   ├── managers.py    # Manager singletons
    │   ├── mcp.py         # MCP server integration
    │   ├── project.py     # Project configuration management
    │   ├── registry.py    # Registry management for installed API appdog
    │   ├── settings.py    # Settings models and utilities
    │   ├── specs.py       # OpenAPI spec parsing
    │   ├── store.py       # API client store implementation
    │   └── utils.py       # Utility functions
    │
    ├── .../             # Installed API appdog
    │   ├── __init__.py    # Package initialization
    │   ├── client.py      # Client implementation
    │   └── models.py      # Pydantic models
    └── (registry.json)    # Auto-generated registry of installed API appdog
```

## License

By contributing to AppDog, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

Thank you for contributing to AppDog!
