# Contributing to mcp-think

Thank you for considering contributing to mcp-think! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ddkang1/mcp-think.git
   cd mcp-think
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Code Style

This project uses:
- [Black](https://black.readthedocs.io/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [Flake8](https://flake8.pycqa.org/) for linting
- [mypy](https://mypy.readthedocs.io/) for type checking

You can run these tools with:
```bash
black src tests
isort src tests
flake8 src tests
mypy src
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting to ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Release Process

1. Update version in `src/mcp_think/__about__.py`
2. Update CHANGELOG.md
3. Create a new GitHub release with the version number as the tag