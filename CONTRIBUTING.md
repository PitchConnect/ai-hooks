# Contributing to Gemini Pre-commit Hook Generator

Thank you for considering contributing to Gemini Pre-commit Hook Generator! This document provides essential guidelines for contributing to this project. For more detailed information, please refer to our [comprehensive contribution guidelines](https://github.com/PitchConnect/contribution-guidelines).

## Table of Contents

- [Quick Start](#quick-start)
- [Code of Conduct](#code-of-conduct)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Project-Specific Guidelines](#project-specific-guidelines)
- [Additional Resources](#additional-resources)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/PitchConnect/gemini-precommit.git
cd gemini-precommit

# Set up development environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Create a feature branch
git checkout develop
git pull
git checkout -b feature/your-feature-name
```

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. We expect all participants to adhere to our Code of Conduct. Please read the [full Code of Conduct document](https://github.com/PitchConnect/contribution-guidelines/blob/main/CODE_OF_CONDUCT.md) before contributing.

## Development Workflow

This project follows the GitFlow workflow:

### Branch Structure

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features or enhancements
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent fixes for production
- `release/*`: Release preparation

### Basic Workflow

1. **Create a feature branch from `develop`**
2. **Make your changes with frequent, small commits**
3. **Push your branch and create a Pull Request to `develop`**
4. **Address review feedback**
5. **After approval, your changes will be merged**

For detailed workflow instructions, see our [GitFlow Workflow Guide](https://github.com/PitchConnect/contribution-guidelines/blob/main/workflow.md).

## Pull Request Process

1. **Ensure your code passes all tests and linting checks**
2. **Update documentation if necessary**
3. **Create a Pull Request with a clear description**
4. **Reference any related issues using keywords like "Fixes #123"**
5. **Wait for review and address any feedback**

For detailed PR guidelines, see our [Pull Request Guide](https://github.com/PitchConnect/contribution-guidelines/blob/main/pull-requests.md).

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Use type hints where appropriate
- Run linting and formatting tools before committing

For detailed coding standards, see our [Coding Standards Guide](https://github.com/PitchConnect/contribution-guidelines/blob/main/coding-standards.md).

## Project-Specific Guidelines

### Setup and Installation

This project uses modern Python packaging with pyproject.toml. To set up your development environment:

```bash
# Install in development mode with all dev dependencies
pip install -e ".[dev]"
```

### Testing

We use pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=gemini_precommit

# Run a specific test
pytest tests/test_analyzer.py
```

### API Key Management

For development, you'll need a Google Gemini API key:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project root with:
   ```
   GOOGLE_GEMINI_API_KEY=your_api_key_here
   ```
3. The code will automatically load this key during development

## Additional Resources

- [Detailed GitFlow Workflow](https://github.com/PitchConnect/contribution-guidelines/blob/main/workflow.md)
- [Coding Standards](https://github.com/PitchConnect/contribution-guidelines/blob/main/coding-standards.md)
- [Testing Guidelines](https://github.com/PitchConnect/contribution-guidelines/blob/main/testing.md)
- [Documentation Guidelines](https://github.com/PitchConnect/contribution-guidelines/blob/main/documentation.md)
- [AI Contribution Guidelines](https://github.com/PitchConnect/contribution-guidelines/blob/main/ai-guidelines.md)
- [Security Guidelines](https://github.com/PitchConnect/contribution-guidelines/blob/main/security.md)

## Working with AI Assistants

If you're using AI tools like GitHub Copilot or ChatGPT, or if you are an AI assistant helping with this project, please refer to our [AI Contribution Guidelines](https://github.com/PitchConnect/contribution-guidelines/blob/main/ai-guidelines.md).

## Issue Management

### Creating Issues

- Use descriptive titles that clearly state the problem or feature
- Include detailed descriptions with context and requirements
- Add appropriate labels (see below)
- Reference related issues or PRs
- **Always include a reference to CONTRIBUTING.md** in new issues
  - Add a note like: "Please follow the guidelines in [CONTRIBUTING.md](../CONTRIBUTING.md) when working on this issue"

### Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working as expected
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on
- `in progress`: Currently being worked on

### Task Tracking

- Use task lists with checkboxes `- [ ]` for tracking progress
- Update these checkboxes as you complete tasks
- If you're an AI assistant, remind users to update task checkboxes

---

Thank you for contributing to Gemini Pre-commit Hook Generator!
