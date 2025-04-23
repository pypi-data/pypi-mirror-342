# Contributing to hatchmat

First off, thank you for considering contributing to hatchmat! It's people like you that make this tool better for everyone :slightly_smiling_face:

## Getting Started

### Prerequisites

- Python 3.8 or newer
- Rust and Cargo installed
- Maturin installed (`pip install maturin>=1.4`)
- Basic knowledge of both Python and Rust

### Dev Environment Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/duriantaco/hatchmat.git
   cd hatchmat
   ```

3. Set up your virtual env

4. Install the package in dev mode:

   ```bash
   pip install -e ".[dev]"
   ```

## Dev Workflow

### Branching Strategy

- `main` branch contains the latest stable release
- Your dev work should be done in feature branches

### Coding Standards

- Follow PEP 8 style guidelines for Python code
- Keep functions focused on a single responsibility. Or at least try to do so.

### Testing

Tests are written using pytest. To run the tests:

```bash
pytest
```

For coverage information:

```bash
pytest --cov=hatchmat
```

#### Writing Tests

- Place tests in the `tests/` directory
- Use fixtures when appropriate to set up test environments
- Test both success and failure cases

### Pull Request Process

1. Create a feature branch for your changes
2. Make your changes and commit them with clear, descriptive commit messages
3. Add or update tests as necessary
4. Ensure all tests pass
5. Update documentation if needed
6. Push your branch to your fork
7. Open a pull request to the main repository
8. Describe your changes in the PR description, linking to any relevant issues

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce
- What you were expecting
- Actual behavior
- Your env details (OS, Python version, Rust version, etc.)
- Any logs or error messages

## Feature Requests

Feature requests are welcome! Please provide:

- A clear description of the feature
- The problem it solves
- Any design ideas or implementation suggestions you may have

## Documentation

Good documentation is very crucial. When adding or changing features:

- Update docstrings
- Update the README.md if necessary
- Consider adding examples for new functionality

## Code of Conduct

Be respectful. Harassment of any kind won't be tolerated.

## License

By contributing to hatchmat, you agree that your contributions will be licensed under the project's MIT license.