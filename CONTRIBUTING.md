# Contributing to AIDomesticCoreAIJ

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported
- Use the bug report template when creating an issue
- Include steps to reproduce, expected behavior, and actual behavior
- Add error logs and environment information

### Proposing Features

- Check existing feature requests first
- Use the feature request template
- Clearly describe the problem and proposed solution
- Explain the use case and benefit

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or poetry
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AIDomesticCoreAIJ.git
cd AIDomesticCoreAIJ

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=aiplatform --cov=sdk

# Run specific test file
pytest tests/test_core.py -v
```

### Code Style

We follow PEP 8 and use the following tools:

```bash
# Format code with black
black aiplatform sdk tests examples

# Check imports with isort
isort aiplatform sdk tests examples

# Lint with flake8
flake8 aiplatform sdk tests

# Type checking with mypy
mypy aiplatform sdk --ignore-missing-imports
```

### Pre-commit Hooks

We recommend using pre-commit hooks to automatically check code quality:

```bash
pip install pre-commit
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Commit Messages

Follow conventional commits:

```
type(scope): subject

body

footer
```

**Types:** feat, fix, docs, style, refactor, test, chore, perf, ci

**Examples:**
- `feat(core): add quantum simulation support`
- `fix(vision): resolve image processing issue`
- `docs: update API documentation`
- `refactor(federated): improve training efficiency`

## Pull Request Process

1. Update documentation for any new features
2. Add or update tests
3. Ensure all tests pass locally
4. Update CHANGELOG.md
5. Ensure code style compliance
6. Request review from maintainers

## Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/name` - Feature branches
- `fix/name` - Bug fix branches
- `docs/name` - Documentation branches
- `refactor/name` - Refactoring branches

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update docs/ folder for comprehensive documentation

## Testing Guidelines

- Write tests for new features
- Maintain >80% code coverage
- Include both unit and integration tests
- Test edge cases and error conditions
- Use descriptive test names

## Release Process

1. Update version number in setup.py
2. Update CHANGELOG.md
3. Merge to main branch
4. Create git tag: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`
6. GitHub Actions will automatically publish to PyPI

## Questions?

- Open an issue with your question
- Check existing documentation
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (See [LICENSE](LICENSE)).

Thank you for contributing! 🎉
