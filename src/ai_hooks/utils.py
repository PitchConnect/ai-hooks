"""Utility functions for the AI Hooks."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


def is_git_repository(path: str = ".") -> bool:
    """Check if the given path is a git repository.

    Args:
        path: Path to check. Defaults to current directory.

    Returns:
        True if the path is a git repository, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() == "true"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_git_root(path: str = ".") -> Optional[str]:
    """Get the root directory of the git repository.

    Args:
        path: Path to start from. Defaults to current directory.

    Returns:
        The root directory of the git repository, or None if not in a git repository.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def is_pre_commit_installed() -> bool:
    """Check if pre-commit is installed.

    Returns:
        True if pre-commit is installed, False otherwise.
    """
    try:
        subprocess.run(
            ["pre-commit", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_pre_commit() -> bool:
    """Install pre-commit if not already installed.

    Returns:
        True if pre-commit is installed successfully, False otherwise.
    """
    if is_pre_commit_installed():
        return True

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pre-commit"],
            check=True,
            capture_output=True,
            text=True,
        )
        return is_pre_commit_installed()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def backup_file(file_path: Union[str, Path]) -> Optional[str]:
    """Create a backup of the given file.

    Args:
        file_path: Path to the file to backup.

    Returns:
        The path to the backup file, or None if backup failed.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return None

    backup_path = f"{file_path}.bak"
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception:
        return None


def check_doc_freshness(repo_path: str = ".") -> List[str]:
    """Check if documentation files are up-to-date.

    This function checks if README.md and other documentation files
    are up-to-date with the codebase.

    Args:
        repo_path: Path to the repository root. Defaults to current directory.

    Returns:
        A list of documentation files that need to be updated.
    """
    repo_path = Path(repo_path)
    outdated_docs = []

    # Check if README.md exists
    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        outdated_docs.append(str(readme_path))
        return outdated_docs

    # Check README.md modification time against code files
    readme_mtime = readme_path.stat().st_mtime
    code_files = []

    # Find code files
    for ext in [".py", ".js", ".ts", ".java", ".go", ".rb", ".php", ".c", ".cpp", ".h", ".hpp"]:
        code_files.extend(repo_path.glob(f"**/*{ext}"))

    # Filter out files in certain directories
    code_files = [
        f for f in code_files
        if not any(part in f.parts for part in [".git", "venv", ".venv", "node_modules", "__pycache__"])
    ]

    # Check if any code file is newer than README.md
    for code_file in code_files:
        if code_file.stat().st_mtime > readme_mtime:
            outdated_docs.append(str(readme_path))
            break

    # Check other documentation files
    doc_dirs = [repo_path / "docs", repo_path / "doc", repo_path / "documentation"]
    for doc_dir in doc_dirs:
        if not doc_dir.exists() or not doc_dir.is_dir():
            continue

        for doc_file in doc_dir.glob("**/*.md"):
            doc_mtime = doc_file.stat().st_mtime
            for code_file in code_files:
                if code_file.stat().st_mtime > doc_mtime:
                    outdated_docs.append(str(doc_file))
                    break

    return outdated_docs
