# Contributing to PEC-DSS

Thank you for considering contributing to PEC-DSS! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct: be respectful, considerate, and constructive in all communications and contributions.

## How to Contribute

### Reporting Bugs

Before submitting a bug report:

1. Check the [GitHub issues](https://github.com/hwk06023/PEC-DSS/issues) to see if the bug has already been reported.
2. Update your copy of the code to the latest version to see if the bug has already been fixed.

When submitting a bug report, please include:

- A clear, descriptive title
- The exact steps to reproduce the bug
- What you expected to happen and what actually happened
- Any error messages or logs
- Your operating system, Python version, and relevant package versions

### Suggesting Improvements

Suggestions for improvements are always welcome! To suggest an improvement:

1. Check existing issues and pull requests to see if your idea has already been suggested.
2. Open a new issue with a clear description of your suggestion.
3. Explain why this improvement would be useful to the project.

### Contributing Code

To contribute code:

1. Fork the repository on GitHub.
2. Clone your fork to your local machine.
3. Create a new branch for your changes.
4. Make your changes, following the coding standards below.
5. Add or update tests and documentation as needed.
6. Run the tests to make sure everything works.
7. Commit your changes.
8. Push to your fork and submit a pull request.

## Development Setup

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS

# Install development dependencies
pip install -e ".[dev]"

# Run tests to make sure everything works
pytest
```

## Coding Standards

Please follow these standards when contributing code:

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style.
- Use [Black](https://black.readthedocs.io/) for code formatting.
- Use [isort](https://pycqa.github.io/isort/) for import sorting.

You can check your code with:

```bash
# Format code
black pec_dss tests

# Sort imports
isort pec_dss tests

# Check for code style issues
flake8 pec_dss tests
```

## Testing

All code contributions should include tests. We use pytest for testing:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=pec_dss tests/
```

## Documentation

All code should be well-documented:

- Add docstrings to all functions, classes, and modules following the [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- Update the documentation in the `docs/` directory if necessary.
- Include example usage for new features.

## Project Structure

The project is structured as follows:

```
pec_dss/
  ├── core/           # Core functionality
  ├── models/         # Model-related code
  ├── utils/          # Utility functions
  ├── __init__.py     # Package initialization
  └── cli.py          # Command-line interface

tests/               # Tests
docs/                # Documentation
examples/            # Example scripts
```

## Pull Request Process

1. Update the documentation with details of your changes.
2. Add tests for any new functionality.
3. Make sure all tests pass.
4. Update the version number in `pec_dss/__init__.py` following [semantic versioning](https://semver.org/).
5. The pull request will be merged once it has been reviewed and approved.

## Questions?

If you have any questions about contributing, please open an issue or contact the project maintainer directly. 