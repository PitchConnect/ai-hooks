"""Tests for the analyzer module."""

import tempfile
from pathlib import Path

from ai_hooks.analyzer import CodebaseAnalyzer, analyze_codebase


def test_analyzer_initialization():
    """Test that the analyzer initializes correctly."""
    analyzer = CodebaseAnalyzer()
    assert analyzer.repo_path.exists()
    assert isinstance(analyzer.file_extensions, set)
    assert isinstance(analyzer.languages, set)
    assert isinstance(analyzer.python_dependencies, set)
    assert isinstance(analyzer.existing_configs, dict)
    assert isinstance(analyzer.ci_workflows, list)


def test_analyze_codebase():
    """Test that analyze_codebase returns a dictionary with the expected keys."""
    results = analyze_codebase()
    assert isinstance(results, dict)
    assert "file_extensions" in results
    assert "languages" in results
    assert "python_dependencies" in results
    assert "existing_configs" in results
    assert "ci_workflows" in results


def test_find_file_extensions():
    """Test that _find_file_extensions finds file extensions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some files with different extensions
        Path(temp_dir, "file.py").touch()
        Path(temp_dir, "file.js").touch()
        Path(temp_dir, "file.md").touch()

        # Create a hidden directory that should be skipped
        hidden_dir = Path(temp_dir, ".hidden")
        hidden_dir.mkdir()
        Path(hidden_dir, "hidden.py").touch()

        analyzer = CodebaseAnalyzer(temp_dir)
        analyzer._find_file_extensions()

        assert "py" in analyzer.file_extensions
        assert "js" in analyzer.file_extensions
        assert "md" in analyzer.file_extensions


def test_detect_languages():
    """Test that _detect_languages detects languages from file extensions."""
    analyzer = CodebaseAnalyzer()
    analyzer.file_extensions = {"py", "js", "md"}
    analyzer._detect_languages()

    assert "python" in analyzer.languages
    assert "javascript" in analyzer.languages
    assert "markdown" in analyzer.languages


def test_find_python_dependencies_requirements_txt():
    """Test that _find_python_dependencies finds dependencies in requirements.txt."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a requirements.txt file
        with open(Path(temp_dir, "requirements.txt"), "w") as f:
            f.write("requests==2.28.1\n")
            f.write("# Comment line\n")
            f.write("flask>=2.0.0\n")

        analyzer = CodebaseAnalyzer(temp_dir)
        analyzer._find_python_dependencies()

        assert "requests" in analyzer.python_dependencies
        assert "flask" in analyzer.python_dependencies


def test_find_existing_configs():
    """Test that _find_existing_configs finds existing configuration files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some configuration files
        Path(temp_dir, ".pre-commit-config.yaml").touch()
        Path(temp_dir, ".flake8").touch()

        analyzer = CodebaseAnalyzer(temp_dir)
        analyzer._find_existing_configs()

        assert "pre-commit" in analyzer.existing_configs
        assert "flake8" in analyzer.existing_configs


def test_find_ci_workflows():
    """Test that _find_ci_workflows finds CI/CD workflow files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create GitHub Actions workflow directory and file
        github_dir = Path(temp_dir, ".github", "workflows")
        github_dir.mkdir(parents=True)
        workflow_file = Path(github_dir, "ci.yml")
        workflow_file.touch()

        analyzer = CodebaseAnalyzer(temp_dir)
        analyzer._find_ci_workflows()

        assert len(analyzer.ci_workflows) == 1
        # On macOS, temporary directories might be created with a /private prefix
        # so we need to compare the resolved paths
        assert workflow_file.resolve() == analyzer.ci_workflows[0].resolve()
