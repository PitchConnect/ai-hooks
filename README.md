# AI Hooks

A tool that uses AI to analyze your codebase and generate customized pre-commit hooks based on your project's specific needs.

## Features

- **Codebase Analysis**: Analyzes your codebase to identify file types, dependencies, and existing configurations
- **CI/CD Integration**: Aligns pre-commit hooks with your CI/CD workflows
- **Custom Hooks**: Creates custom hooks for checking documentation freshness
- **Non-interactive Mode**: Supports automation in CI/CD pipelines
- **Fallback Mechanisms**: Provides robust error handling with fallback configurations

## Installation

```bash
pip install ai-hooks
```

## Quick Start

```bash
# Generate pre-commit hooks interactively
ai-hooks generate

# Generate pre-commit hooks non-interactively
ai-hooks generate --non-interactive

# Generate and install pre-commit hooks
ai-hooks generate --install
```

## Requirements

- Python 3.8+
- Google Gemini API key (set as `AI_HOOKS_API_KEY` environment variable)

## Configuration

The generator uses the following environment variables:

- `AI_HOOKS_API_KEY`: Your Google Gemini API key

You can set these in a `.env` file in your project root.

## Usage Examples

### Basic Usage

```bash
ai-hooks generate
```

This will analyze your codebase, generate a customized pre-commit configuration, and prompt for confirmation before applying changes.

### Non-interactive Mode

```bash
ai-hooks generate --non-interactive
```

This will generate and apply changes without prompting for confirmation, ideal for automation.

### Additional Options

```bash
ai-hooks generate --non-interactive --install
```

The `--install` flag will automatically install the hooks after generating the configuration.

## How It Works

1. **Codebase Analysis**: The tool scans your codebase to identify file types, dependencies, and existing configurations.
2. **CI/CD Integration**: It analyzes your CI/CD workflows to ensure alignment between pre-commit hooks and CI checks.
3. **LLM-Powered Generation**: Using AI, it generates a customized pre-commit configuration based on the analysis.
4. **Custom Hooks**: It creates custom hooks for project-specific needs like documentation freshness checks.
5. **Configuration Application**: It applies the generated configuration to your project.

## Contributing

Please see our [Contributing Guidelines](CONTRIBUTING.md) for information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
