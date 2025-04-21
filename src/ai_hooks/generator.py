"""Pre-commit hook generator for the AI Hooks.

This module generates pre-commit hook configurations based on codebase analysis
and AI-powered responses.
"""

import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional


from ai_hooks.analyzer import analyze_codebase
from ai_hooks.ai_client import generate_precommit_config
from ai_hooks.logging import get_logger


class PrecommitGenerator:
    """Generates pre-commit hook configurations."""

    def __init__(
        self, repo_path: str = ".", api_key: Optional[str] = None, non_interactive: bool = False
    ) -> None:
        """Initialize the generator with the repository path.

        Args:
            repo_path: Path to the repository root. Defaults to current directory.
            api_key: Google Gemini API key. If not provided, will try to load from
                environment variable GOOGLE_GEMINI_API_KEY.
            non_interactive: Whether to run in non-interactive mode. Defaults to False.
        """
        self.logger = get_logger("generator")
        self.logger.info(f"Initializing pre-commit generator for repository at {repo_path}")

        self.repo_path = Path(repo_path).resolve()
        self.api_key = api_key
        self.non_interactive = non_interactive
        self.config_path = self.repo_path / ".pre-commit-config.yaml"
        self.logger.debug(f"Config path set to {self.config_path}")
        self.logger.debug(f"Non-interactive mode: {self.non_interactive}")

        self.analysis_results: Dict[str, Any] = {}
        self.generated_config: Dict[str, Any] = {}

    def generate(self) -> Dict[str, Any]:
        """Generate pre-commit hooks for the repository.

        Returns:
            A dictionary containing the generated pre-commit configuration.
        """
        self.logger.info("Starting pre-commit hook generation process")

        self.logger.info("Analyzing codebase...")
        start_time = time.time()
        self.analysis_results = analyze_codebase(str(self.repo_path))
        elapsed_time = time.time() - start_time
        self.logger.debug(f"Codebase analysis completed in {elapsed_time:.2f} seconds")

        self.logger.info("Generating pre-commit configuration...")
        start_time = time.time()
        self.generated_config = generate_precommit_config(self.analysis_results, self.api_key)
        elapsed_time = time.time() - start_time
        self.logger.debug(f"Configuration generation completed in {elapsed_time:.2f} seconds")
        self.logger.info("Pre-commit hook generation completed successfully")

        return self.generated_config

    def apply_config(self, install: bool = False) -> bool:
        """Apply the generated configuration to the repository.

        Args:
            install: Whether to install the hooks after applying the configuration.

        Returns:
            True if the configuration was applied successfully, False otherwise.
        """
        self.logger.info("Applying generated configuration to repository")

        if not self.generated_config:
            self.logger.error("No configuration generated. Run generate() first.")
            print("No configuration generated. Run generate() first.")
            return False

        yaml_content = self.generated_config.get("yaml_content", "")
        if not yaml_content:
            self.logger.error("Generated configuration is empty")
            print("Generated configuration is empty.")
            return False

        # If the file exists and we're in interactive mode, ask for confirmation
        if self.config_path.exists() and not self.non_interactive:
            self.logger.info(f"Existing configuration found at {self.config_path}")
            self.logger.debug(f"Generated configuration length: {len(yaml_content)} characters")

            print(f"\nExisting configuration found at {self.config_path}")
            print("\nGenerated configuration:")
            print("-" * 80)
            print(yaml_content)
            print("-" * 80)

            response = input("\nDo you want to replace the existing configuration? (y/n): ")
            if response.lower() != "y":
                self.logger.info("User chose not to apply the configuration")
                print("Configuration not applied.")
                return False

            self.logger.info("User confirmed configuration replacement")

        # Write the configuration to the file
        try:
            self.logger.info(f"Writing configuration to {self.config_path}")
            with open(self.config_path, "w", encoding="utf-8") as f:
                f.write(yaml_content)
            self.logger.info(f"Configuration successfully written to {self.config_path}")
            print(f"Configuration written to {self.config_path}")
        except Exception as e:
            error_msg = f"Failed to write configuration: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(f"Full error details: {e}", exc_info=True)
            print(error_msg)
            return False

        # Install the hooks if requested
        if install:
            self.logger.info("Installing pre-commit hooks")
            return self._install_hooks()

        self.logger.info("Configuration applied successfully")
        return True

    def _install_hooks(self) -> bool:
        """Install the pre-commit hooks.

        Returns:
            True if the hooks were installed successfully, False otherwise.
        """
        self.logger.info("Installing pre-commit hooks")
        try:
            print("Installing pre-commit hooks...")
            self.logger.debug(f"Running 'pre-commit install' in {self.repo_path}")
            start_time = time.time()
            result = subprocess.run(
                ["pre-commit", "install"],
                cwd=str(self.repo_path),
                check=True,
                capture_output=True,
                text=True,
            )
            elapsed_time = time.time() - start_time
            self.logger.debug(f"Hook installation completed in {elapsed_time:.2f} seconds")
            self.logger.debug(f"Installation output: {result.stdout}")
            print(result.stdout)
            self.logger.info("Pre-commit hooks installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to install hooks: {e.stderr}"
            self.logger.error(error_msg)
            self.logger.debug(f"Command failed with return code {e.returncode}")
            print(error_msg)
            return False
        except Exception as e:
            error_msg = f"Failed to install hooks: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(f"Full error details: {e}", exc_info=True)
            print(error_msg)
            return False


def generate_hooks(
    repo_path: str = ".",
    api_key: Optional[str] = None,
    non_interactive: bool = False,
    install: bool = False,
) -> Dict[str, Any]:
    """Generate pre-commit hooks for the repository.

    Args:
        repo_path: Path to the repository root. Defaults to current directory.
        api_key: Google Gemini API key. If not provided, will try to load from
            environment variable GOOGLE_GEMINI_API_KEY.
        non_interactive: Whether to run in non-interactive mode. Defaults to False.
        install: Whether to install the hooks after generating. Defaults to False.

    Returns:
        A dictionary containing the generated pre-commit configuration.
    """
    generator = PrecommitGenerator(repo_path, api_key, non_interactive)
    config = generator.generate()

    if generator.apply_config(install):
        return {
            "success": True,
            "config": config,
            "config_path": str(generator.config_path),
        }
    else:
        return {
            "success": False,
            "config": config,
            "error": "Failed to apply configuration",
        }
