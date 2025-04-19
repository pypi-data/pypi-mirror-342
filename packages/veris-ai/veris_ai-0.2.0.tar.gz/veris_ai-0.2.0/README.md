# Veris AI Python SDK

A Python package for Veris AI tools with simulation capabilities.

## Installation

You can install the package using `uv`:

```bash
# Install the package
uv add veris-ai

# Install with development dependencies
uv add "veris-ai[dev]"
```

## Environment Setup

The package requires the following environment variables:

```bash
# Required: URL for the mock endpoint
VERIS_MOCK_ENDPOINT_URL=http://your-mock-endpoint.com

# Optional: Timeout in seconds (default: 30.0)
VERIS_MOCK_TIMEOUT=30.0

# Optional: Set to "simulation" to enable mock mode
ENV=simulation
```

## Python Version

This project requires Python 3.11 or higher. We use [pyenv](https://github.com/pyenv/pyenv) for Python version management.

To set up the correct Python version:

```bash
# Install Python 3.11.0 using pyenv
pyenv install 3.11.0

# Set the local Python version for this project
pyenv local 3.11.0
```

## Usage

```python
from veris_ai import veris

@veris.mock()
async def your_function(param1: str, param2: int) -> dict:
    """
    Your function documentation here.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        A dictionary containing the results
    """
    # Your implementation here
    return {"result": "actual implementation"}
```

When `ENV=simulation` is set, the decorator will:
1. Capture the function signature, type hints, and docstring
2. Send this information to the mock endpoint
3. Convert the mock response to the expected return type
4. Return the mock result

When not in simulation mode, the original function will be executed normally.

## Development

This project uses `pyproject.toml` for dependency management and `uv` for package installation.

### Development Dependencies

To install the package with development dependencies:

```bash
uv add "veris-ai[dev]"
```

This will install the following development tools:
- **Ruff**: Fast Python linter
- **pytest**: Testing framework
- **pytest-asyncio**: Async support for pytest
- **pytest-cov**: Coverage reporting for pytest
- **black**: Code formatter
- **mypy**: Static type checker
- **pre-commit**: Git hooks for code quality

### Code Quality

This project uses [Ruff](https://github.com/charliermarsh/ruff) for linting and code quality checks. Ruff is a fast Python linter written in Rust.

To run Ruff:

```bash
ruff check .
```

To automatically fix issues:

```bash
ruff check --fix .
```

The Ruff configuration is defined in `pyproject.toml` under the `[tool.ruff]` section.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 