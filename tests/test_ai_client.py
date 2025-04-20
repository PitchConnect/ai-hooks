"""Tests for the AI client module."""

import json
import os
from unittest import mock

import pytest

from ai_hooks.ai_client import AIClient, generate_precommit_config


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Set a mock API key in the environment."""
    monkeypatch.setenv("AI_HOOKS_API_KEY", "test_api_key")


@pytest.fixture
def mock_gemini_response():
    """Create a mock Gemini API response."""
    class MockResponse:
        @property
        def text(self):
            return """```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
```"""
    return MockResponse()


def test_ai_client_initialization(mock_env_api_key):
    """Test that the AI client initializes correctly with an environment variable."""
    client = AIClient()
    assert client.api_key == "test_api_key"


def test_ai_client_initialization_with_parameter():
    """Test that the AI client initializes correctly with a parameter."""
    client = AIClient(api_key="parameter_api_key")
    assert client.api_key == "parameter_api_key"


def test_ai_client_initialization_no_api_key():
    """Test that the AI client raises an error when no API key is provided."""
    with mock.patch.dict(os.environ, clear=True):
        with pytest.raises(ValueError):
            AIClient()


def test_create_prompt():
    """Test that _create_prompt creates a prompt with the expected content."""
    client = AIClient(api_key="test_api_key")
    analysis_results = {
        "file_extensions": ["py", "md"],
        "languages": ["python", "markdown"],
        "python_dependencies": ["requests", "flask"],
        "existing_configs": {"pre-commit": "/path/to/.pre-commit-config.yaml"},
        "ci_workflows": ["/path/to/.github/workflows/ci.yml"],
    }
    
    prompt = client._create_prompt(analysis_results)
    
    assert "File extensions: py, md" in prompt
    assert "Programming languages: python, markdown" in prompt
    assert "Python dependencies: requests, flask" in prompt
    assert "pre-commit" in prompt
    assert "ci.yml" in prompt


@mock.patch("google.generativeai.GenerativeModel.generate_content")
def test_call_ai_service(mock_generate_content, mock_gemini_response):
    """Test that _call_ai_service calls the Gemini API and returns the response."""
    mock_generate_content.return_value = mock_gemini_response
    
    client = AIClient(api_key="test_api_key")
    response = client._call_ai_service("test prompt")
    
    mock_generate_content.assert_called_once_with("test prompt")
    assert "```yaml" in response
    assert "pre-commit-hooks" in response


@mock.patch("google.generativeai.GenerativeModel.generate_content")
def test_call_ai_service_error(mock_generate_content):
    """Test that _call_ai_service handles errors correctly."""
    mock_generate_content.side_effect = Exception("API error")
    
    client = AIClient(api_key="test_api_key")
    with pytest.raises(Exception) as excinfo:
        client._call_ai_service("test prompt")
    
    assert "Failed to call AI service" in str(excinfo.value)


def test_parse_response():
    """Test that _parse_response extracts YAML content correctly."""
    client = AIClient(api_key="test_api_key")
    response = """```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
```"""
    
    result = client._parse_response(response)
    
    assert "yaml_content" in result
    assert "raw_response" in result
    assert "pre-commit-hooks" in result["yaml_content"]
    assert "```yaml" not in result["yaml_content"]
    assert "```" not in result["yaml_content"]


@mock.patch("ai_hooks.ai_client.AIClient.generate_precommit_config")
def test_generate_precommit_config(mock_generate_precommit_config):
    """Test that generate_precommit_config creates a client and calls generate_precommit_config."""
    mock_generate_precommit_config.return_value = {"yaml_content": "test content"}
    
    analysis_results = {"test": "data"}
    result = generate_precommit_config(analysis_results, api_key="test_api_key")
    
    mock_generate_precommit_config.assert_called_once_with(analysis_results)
    assert result == {"yaml_content": "test content"}
