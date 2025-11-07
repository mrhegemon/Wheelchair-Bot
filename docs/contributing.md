# Contributing to Wheelchair Bot

Thank you for your interest in contributing to Wheelchair Bot! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Node version)

### Suggesting Features

Feature requests are welcome! Please create an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
2. **Make your changes** following the coding standards below
3. **Add tests** for any new functionality
4. **Ensure all tests pass**
5. **Update documentation** as needed
6. **Submit a pull request**

## Development Setup

See [Getting Started Guide](docs/getting-started.md) for setup instructions.

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Format code with `black`
- Lint with `ruff`
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Write tests for new functionality

### JavaScript/React

- Follow ESLint configuration
- Use functional components and hooks
- Write clear, descriptive variable names
- Keep components small and focused
- Use proper prop types

## Testing

### Backend Tests

```bash
cd packages/backend
pytest
```

### Shared Library Tests

```bash
cd packages/shared
pytest
```

### Frontend

Currently, no automated tests for frontend. Manual testing required.

## Commit Messages

Use clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add movement speed control to API

- Add speed parameter to move endpoint
- Update tests for speed validation
- Update documentation

Fixes #123
```

## Documentation

Update documentation when you:
- Add new features
- Change existing functionality
- Add new dependencies
- Change configuration

## Questions?

Feel free to create an issue for any questions about contributing.

Thank you for contributing to Wheelchair Bot! 🦽
