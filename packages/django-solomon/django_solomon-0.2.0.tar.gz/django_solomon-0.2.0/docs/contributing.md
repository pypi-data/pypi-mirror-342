---
hide:
  - navigation
---

# Contributing to django-solomon

Thank you for your interest in contributing to django-solomon! This guide will help you get started with the development process.

## Development Environment Setup

### Prerequisites

Before setting up the development environment, ensure you have:

- Python 3.10 or higher
- Git
- [uv](https://github.com/astral-sh/uv) for dependency management
- [just](https://github.com/casey/just) for running commands

### Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://codeberg.org/oliverandrich/django-solomon.git
cd django-solomon
```

2. Set up the development environment using the bootstrap command:

```bash
just bootstrap
```

This command will:
- Initialize a git repository
- Install all dependencies
- Set up pre-commit hooks

If you already have a cloned repository, you can install dependencies with:

```bash
just upgrade
```

## Development Workflow

### Running Tests

To run the test suite with coverage reporting:

```bash
just test
```

To run the full test suite across all supported Python and Django versions:

```bash
just test-all
```

### Linting and Code Quality

The project uses Ruff for linting and formatting. To run the linters:

```bash
just lint
```

This will run all pre-commit hooks, including Ruff linting and formatting.

### Documentation

To serve the documentation locally:

```bash
just serve-docs
```

This will start a local server at http://127.0.0.1:8000/ where you can preview the documentation.

## Coding Standards

### Python Style Guide

The project follows the PEP 8 style guide with some modifications:

- Maximum line length is 120 characters
- Uses double quotes for strings
- Does NOT use relative imports for internal modules

Ruff is configured to enforce these standards. The configuration can be found in `pyproject.toml`.

### Type Annotations

The project uses type annotations and mypy for type checking. Please add type annotations to all new code.

### Testing

All new features and bug fixes should include tests. The project uses pytest for testing.

- Place tests in the `tests/` directory
- Ensure tests are isolated and don't depend on external services
- Aim for high test coverage

## Pull Request Process

1. Fork the repository on [Codeberg](https://codeberg.org/oliverandrich/django-solomon)
2. Create a new branch for your feature or bug fix
3. Make your changes, following the coding standards
4. Add tests for your changes
5. Run the test suite to ensure all tests pass
6. Update the documentation if necessary
7. Submit a pull request to the main repository

### Pull Request Guidelines

- Keep pull requests focused on a single feature or bug fix
- Include a clear description of the changes
- Reference any related issues
- Ensure all tests pass and code quality checks succeed
- Update the CHANGELOG.md file if your changes are user-facing

## Release Process

The project follows [Semantic Versioning](https://semver.org/). The release process is handled by the maintainers.

## Getting Help

If you have questions or need help with the development process, you can:

- Open an issue on [Codeberg](https://codeberg.org/oliverandrich/django-solomon/issues)
- Contact the maintainers directly

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We aim to foster an inclusive and welcoming community.
