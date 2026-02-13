# Contributing to ISE Switch Session Manager

Thank you for your interest in contributing to the ISE Switch Session Manager! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project follows a Code of Conduct that all contributors are expected to adhere to:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/webapp-ise-switch-sessions.git
   cd webapp-ise-switch-sessions
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/dagolovach/webapp-ise-switch-sessions.git
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies (optional):
   ```bash
   pip install black pylint autopep8
   ```

4. Set up your `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix bugs in the existing code
- **Features**: Add new features or enhance existing ones
- **Documentation**: Improve documentation, add examples, fix typos
- **Tests**: Add or improve test coverage
- **Code Quality**: Refactor code, improve performance, add type hints

### Development Workflow

1. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Your Changes**:
   - Write clean, readable code
   - Follow the coding standards (see below)
   - Add docstrings to new functions/classes
   - Update documentation if needed

3. **Test Your Changes**:
   - Test your changes thoroughly
   - Ensure existing functionality still works
   - Add new tests if applicable

4. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

   Use clear, descriptive commit messages:
   - `feat: Add new feature X`
   - `fix: Resolve issue with Y`
   - `docs: Update README with Z`
   - `refactor: Improve code quality in module A`

5. **Stay Up to Date**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

6. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**:
   - Go to GitHub and create a Pull Request
   - Provide a clear description of your changes
   - Reference any related issues

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Formatting

We recommend using `black` for code formatting:

```bash
black *.py
```

### Type Hints

Add type hints to function signatures:

```python
def get_group_id() -> Dict[str, str]:
    """Retrieve all endpoint groups."""
    pass
```

### Docstrings

All functions and classes should have comprehensive docstrings:

```python
def update_endpoint_group(mac: str, ise_group_id: str) -> requests.Response:
    """
    Update the endpoint group assignment in ISE.

    Args:
        mac (str): MAC address of the endpoint to update.
        ise_group_id (str): The ID of the new ISE endpoint group.

    Returns:
        requests.Response: HTTP response object from the PUT request.

    Raises:
        requests.exceptions.RequestException: If the API request fails.

    Example:
        >>> response = update_endpoint_group('AA:BB:CC:DD:EE:FF', 'group-id')
        >>> print(response.status_code)
        200
    """
    pass
```

### Code Organization

- Keep functions focused and single-purpose
- Avoid deep nesting (max 3-4 levels)
- Use meaningful variable names
- Add comments for complex logic
- Group related functionality together

### Error Handling

- Use specific exception types, not bare `except:`
- Provide informative error messages
- Log errors appropriately

```python
try:
    result = some_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
```

## Testing

### Manual Testing

Before submitting a PR:

1. Test the web interface thoroughly
2. Test with different input formats
3. Verify error handling works correctly
4. Check that logging is appropriate

### Test Checklist

- [ ] Code runs without errors
- [ ] All existing functionality still works
- [ ] New features work as expected
- [ ] Error cases are handled gracefully
- [ ] No sensitive data is logged or exposed
- [ ] Documentation is updated

## Submitting Changes

### Pull Request Guidelines

When submitting a pull request:

1. **Title**: Use a clear, descriptive title
   - Good: "Add support for multiple ISE servers"
   - Bad: "Update code"

2. **Description**: Include:
   - What changes were made
   - Why the changes were necessary
   - Any relevant issue numbers (e.g., "Fixes #123")
   - Screenshots (for UI changes)

3. **Checklist**:
   - [ ] Code follows the style guidelines
   - [ ] Docstrings are added/updated
   - [ ] README is updated if needed
   - [ ] No sensitive data is committed
   - [ ] Changes have been tested

### Review Process

- Maintainers will review your PR
- Be responsive to feedback
- Make requested changes promptly
- Keep discussions focused and professional

## Reporting Bugs

### Before Submitting a Bug Report

- Check if the bug has already been reported
- Verify you're using the latest version
- Collect relevant information

### Bug Report Template

When reporting a bug, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**:
   1. Step 1
   2. Step 2
   3. ...
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - Python version
   - Flask version
   - Operating system
   - ISE version
6. **Logs/Screenshots**: Any relevant error messages or screenshots

## Feature Requests

We welcome feature requests! When submitting a feature request:

1. **Use Case**: Explain the problem you're trying to solve
2. **Proposed Solution**: Describe your proposed solution
3. **Alternatives**: List any alternative solutions you've considered
4. **Additional Context**: Add any other context or screenshots

## Questions?

If you have questions:

- Open an issue with the "question" label
- Check the README for documentation
- Review existing issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to ISE Switch Session Manager! 🎉
