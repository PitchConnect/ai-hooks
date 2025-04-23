"""Codebase analyzer for the AI Hooks.

This module analyzes a codebase to identify file types, dependencies,
and existing configurations to inform the generation of pre-commit hooks.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set

from ai_hooks.logging import get_logger


class CodebaseAnalyzer:
    """Analyzes a codebase to inform pre-commit hook generation."""

    def __init__(self, repo_path: str = ".") -> None:
        """Initialize the analyzer with the repository path.

        Args:
            repo_path: Path to the repository root. Defaults to current directory.
        """
        self.logger = get_logger("analyzer")
        self.repo_path = Path(repo_path).resolve()
        self.logger.info(f"Initializing analyzer for repository at {self.repo_path}")
        self.file_extensions: Set[str] = set()
        self.languages: Set[str] = set()
        self.python_dependencies: Set[str] = set()
        self.existing_configs: Dict[str, Path] = {}
        self.ci_workflows: List[Path] = []

    def analyze(self) -> Dict[str, Any]:
        """Analyze the codebase and return the results.

        Returns:
            A dictionary containing analysis results.
        """
        self.logger.info("Starting codebase analysis")

        self.logger.debug("Finding file extensions")
        self._find_file_extensions()

        self.logger.debug("Detecting languages")
        self._detect_languages()

        self.logger.debug("Finding Python dependencies")
        self._find_python_dependencies()

        self.logger.debug("Finding existing configurations")
        self._find_existing_configs()

        self.logger.debug("Finding CI/CD workflows")
        self._find_ci_workflows()

        results: Dict[str, Any] = {
            "file_extensions": sorted(list(self.file_extensions)),
            "languages": sorted(list(self.languages)),
            "python_dependencies": sorted(list(self.python_dependencies)),
            "existing_configs": {k: str(v) for k, v in self.existing_configs.items()},
            "ci_workflows": [str(p) for p in self.ci_workflows],
        }

        self.logger.info(
            f"Analysis complete. Found {len(self.file_extensions)} file extensions, "
            f"{len(self.languages)} languages, {len(self.python_dependencies)} Python dependencies, "
            f"{len(self.existing_configs)} existing configs, and {len(self.ci_workflows)} CI workflows"
        )
        self.logger.debug(f"Analysis results: {results}")

        return results

    def _find_file_extensions(self) -> None:
        """Find all file extensions in the repository."""
        self.logger.trace(f"Walking directory tree starting at {self.repo_path}")  # type: ignore
        for root, _, files in os.walk(self.repo_path):
            # Skip hidden directories and virtual environments
            if any(
                (part.startswith(".")
                 or part in ("venv", ".venv", "env", "node_modules", "__pycache__"))
                for part in Path(root).parts
            ):
                self.logger.trace(f"Skipping directory {root}")  # type: ignore
                continue

            self.logger.trace(f"Processing {len(files)} files in {root}")  # type: ignore
            for file in files:
                # Skip hidden files
                if file.startswith("."):
                    self.logger.trace(f"Skipping hidden file {file}")  # type: ignore
                    continue

                ext = os.path.splitext(file)[1].lower()
                if ext:
                    self.logger.trace(f"Found file extension: {ext[1:]} in file {file}")  # type: ignore
                    self.file_extensions.add(ext[1:])  # Remove the leading dot

    def _detect_languages(self) -> None:
        """Detect programming languages used in the repository."""
        extension_to_language = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "jsx": "javascript",
            "tsx": "typescript",
            "rb": "ruby",
            "go": "go",
            "java": "java",
            "kt": "kotlin",
            "rs": "rust",
            "c": "c",
            "cpp": "c++",
            "h": "c",
            "hpp": "c++",
            "cs": "c#",
            "php": "php",
            "swift": "swift",
            "scala": "scala",
            "clj": "clojure",
            "ex": "elixir",
            "exs": "elixir",
            "hs": "haskell",
            "sh": "shell",
            "bash": "shell",
            "zsh": "shell",
            "fish": "shell",
            "ps1": "powershell",
            "bat": "batch",
            "cmd": "batch",
            "sql": "sql",
            "r": "r",
            "dart": "dart",
            "lua": "lua",
            "pl": "perl",
            "pm": "perl",
            "groovy": "groovy",
            "yaml": "yaml",
            "yml": "yaml",
            "json": "json",
            "xml": "xml",
            "html": "html",
            "css": "css",
            "scss": "scss",
            "sass": "sass",
            "less": "less",
            "md": "markdown",
            "markdown": "markdown",
            "rst": "restructuredtext",
            "toml": "toml",
            "ini": "ini",
            "cfg": "ini",
            "conf": "ini",
            "dockerfile": "dockerfile",
            "tf": "terraform",
            "hcl": "hcl",
        }

        for ext in self.file_extensions:
            if ext in extension_to_language:
                self.languages.add(extension_to_language[ext])

    def _find_python_dependencies(self) -> None:
        """Find Python dependencies in the repository."""
        # Check requirements.txt
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            self._parse_requirements_txt(requirements_file)

        # Check setup.py
        setup_py = self.repo_path / "setup.py"
        if setup_py.exists():
            self._parse_setup_py(setup_py)

        # Check pyproject.toml
        pyproject_toml = self.repo_path / "pyproject.toml"
        if pyproject_toml.exists():
            self._parse_pyproject_toml(pyproject_toml)

        # Check Pipfile
        pipfile = self.repo_path / "Pipfile"
        if pipfile.exists():
            self._parse_pipfile(pipfile)

    def _parse_requirements_txt(self, file_path: Path) -> None:
        """Parse requirements.txt file to extract dependencies.

        Args:
            file_path: Path to the requirements.txt file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    # Extract package name (ignore version specifiers)
                    match = re.match(r"^([a-zA-Z0-9_.-]+)", line)
                    if match:
                        self.python_dependencies.add(match.group(1).lower())
        except Exception:
            # Silently fail if we can't parse the file
            pass

    def _parse_setup_py(self, file_path: Path) -> None:
        """Parse setup.py file to extract dependencies.

        Args:
            file_path: Path to the setup.py file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Look for install_requires list
                match = re.search(r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL)
                if match:
                    deps_str = match.group(1)
                    # Extract package names from quotes
                    for dep_match in re.finditer(r"['\"]([a-zA-Z0-9_.-]+)['\"]", deps_str):
                        self.python_dependencies.add(dep_match.group(1).lower())
        except Exception:
            # Silently fail if we can't parse the file
            pass

    def _parse_pyproject_toml(self, file_path: Path) -> None:
        """Parse pyproject.toml file to extract dependencies.

        Args:
            file_path: Path to the pyproject.toml file.
        """
        try:
            import tomli

            with open(file_path, "rb") as f:
                data = tomli.load(f)
                # Check for dependencies in different possible locations
                deps = []
                if "project" in data and "dependencies" in data["project"]:
                    deps.extend(data["project"]["dependencies"])
                elif "tool" in data:
                    if "poetry" in data["tool"] and "dependencies" in data["tool"]["poetry"]:
                        deps.extend(data["tool"]["poetry"]["dependencies"].keys())
                    elif "pdm" in data["tool"] and "dependencies" in data["tool"]["pdm"]:
                        deps.extend(data["tool"]["pdm"]["dependencies"])

                for dep in deps:
                    # Extract package name (ignore version specifiers)
                    match = re.match(r"^([a-zA-Z0-9_.-]+)", dep)
                    if match:
                        self.python_dependencies.add(match.group(1).lower())
        except ImportError:
            # tomli not available, try a simple regex approach
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Look for dependencies sections
                    for section in ["dependencies", "tool.poetry.dependencies", "tool.pdm.dependencies"]:
                        section_pattern = rf"{section}\s*=\s*\[(.*?)\]"
                        match = re.search(section_pattern, content, re.DOTALL)
                        if match:
                            deps_str = match.group(1)
                            # Extract package names from quotes
                            for dep_match in re.finditer(r"['\"]([a-zA-Z0-9_.-]+)['\"]", deps_str):
                                self.python_dependencies.add(dep_match.group(1).lower())
            except Exception:
                # Silently fail if we can't parse the file
                pass
        except Exception:
            # Silently fail if we can't parse the file
            pass

    def _parse_pipfile(self, file_path: Path) -> None:
        """Parse Pipfile to extract dependencies.

        Args:
            file_path: Path to the Pipfile.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Look for packages section
                match = re.search(r"\[packages\](.*?)(\[|\Z)", content, re.DOTALL)
                if match:
                    packages_section = match.group(1)
                    # Extract package names
                    for line in packages_section.split("\n"):
                        line = line.strip()
                        if "=" in line:
                            package = line.split("=")[0].strip()
                            if package:
                                self.python_dependencies.add(package.lower())
        except Exception:
            # Silently fail if we can't parse the file
            pass

    def _find_existing_configs(self) -> None:
        """Find existing configuration files in the repository."""
        config_files = {
            "pre-commit": ".pre-commit-config.yaml",
            "flake8": ".flake8",
            "black": "pyproject.toml",  # Black config is in pyproject.toml
            "isort": ".isort.cfg",
            "mypy": "mypy.ini",
            "pylint": ".pylintrc",
            "eslint": ".eslintrc.js",
            "prettier": ".prettierrc",
            "stylelint": ".stylelintrc",
        }

        for config_name, filename in config_files.items():
            config_path = self.repo_path / filename
            if config_path.exists():
                self.existing_configs[config_name] = config_path

        # Check for pyproject.toml with tool configurations
        pyproject_path = self.repo_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for tool in ["black", "isort", "mypy", "flake8", "pylint"]:
                        if f"tool.{tool}" in content:
                            self.existing_configs[tool] = pyproject_path
            except Exception:
                # Silently fail if we can't read the file
                pass

    def _find_ci_workflows(self) -> None:
        """Find CI/CD workflow files in the repository."""
        # GitHub Actions
        github_workflows = self.repo_path / ".github" / "workflows"
        if github_workflows.exists() and github_workflows.is_dir():
            for file in github_workflows.glob("*.yml"):
                self.ci_workflows.append(file)
            for file in github_workflows.glob("*.yaml"):
                self.ci_workflows.append(file)

        # GitLab CI
        gitlab_ci = self.repo_path / ".gitlab-ci.yml"
        if gitlab_ci.exists():
            self.ci_workflows.append(gitlab_ci)

        # CircleCI
        circleci = self.repo_path / ".circleci" / "config.yml"
        if circleci.exists():
            self.ci_workflows.append(circleci)

        # Travis CI
        travis = self.repo_path / ".travis.yml"
        if travis.exists():
            self.ci_workflows.append(travis)

        # Azure Pipelines
        azure = self.repo_path / "azure-pipelines.yml"
        if azure.exists():
            self.ci_workflows.append(azure)


def analyze_codebase(repo_path: str = ".") -> Dict[str, object]:
    """Analyze the codebase and return the results.

    Args:
        repo_path: Path to the repository root. Defaults to current directory.

    Returns:
        A dictionary containing analysis results.
    """
    analyzer = CodebaseAnalyzer(repo_path)
    return analyzer.analyze()
