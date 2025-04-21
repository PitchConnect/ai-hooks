"""Command-line interface for the AI Hooks."""

import sys
import time
from typing import Optional

import click

from ai_hooks.generator import generate_hooks
from ai_hooks.logging import get_logger, setup_logging
from ai_hooks.utils import get_git_root, is_git_repository, is_pre_commit_installed, install_pre_commit


@click.group()
@click.version_option()
@click.option(
    "--log-level",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default="INFO",
    help="Set the logging level.",
    envvar="AI_HOOKS_LOG_LEVEL",
)
@click.option(
    "--log-file",
    type=click.Path(),
    help="Log to this file in addition to the console.",
    envvar="AI_HOOKS_LOG_FILE",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Suppress console logging.",
)
def cli(log_level: str, log_file: Optional[str], quiet: bool) -> None:
    """AI Hooks.

    A tool that uses AI to analyze your codebase and generate
    customized pre-commit hooks based on your project's specific needs.
    """
    # Set up logging
    setup_logging(level=log_level, log_file=log_file, log_to_console=not quiet)
    logger = get_logger()
    logger.debug(f"Logging initialized at level {log_level}")
    if log_file:
        logger.debug(f"Logging to file: {log_file}")
    if quiet:
        logger.debug("Console logging suppressed")


@cli.command()
@click.option(
    "--repo-path",
    "-p",
    default=".",
    help="Path to the repository root. Defaults to current directory.",
)
@click.option(
    "--api-key",
    "-k",
    help="Google Gemini API key. If not provided, will try to load from environment variable GOOGLE_GEMINI_API_KEY.",
)
@click.option(
    "--non-interactive",
    "-n",
    is_flag=True,
    help="Run in non-interactive mode. Will not prompt for confirmation.",
)
@click.option(
    "--install",
    "-i",
    is_flag=True,
    help="Install the hooks after generating.",
)
def generate(
    repo_path: str = ".",
    api_key: Optional[str] = None,
    non_interactive: bool = False,
    install: bool = False,
) -> None:
    """Generate pre-commit hooks for the repository."""
    logger = get_logger("cli")
    logger.info(f"Starting pre-commit hook generation for {repo_path}")

    # Check if the path is a git repository
    logger.debug(f"Checking if {repo_path} is a git repository")
    if not is_git_repository(repo_path):
        logger.error(f"{repo_path} is not a git repository")
        click.echo(f"Error: {repo_path} is not a git repository.")
        sys.exit(1)

    # Get the repository root
    logger.debug(f"Getting git repository root from {repo_path}")
    git_root = get_git_root(repo_path)
    if not git_root:
        logger.error(f"Could not determine git repository root from {repo_path}")
        click.echo(f"Error: Could not determine git repository root from {repo_path}.")
        sys.exit(1)
    logger.debug(f"Repository root: {git_root}")

    # Check if pre-commit is installed
    if install:
        logger.debug("Checking if pre-commit is installed")
        if not is_pre_commit_installed():
            logger.info("pre-commit is not installed, attempting to install")
            click.echo("pre-commit is not installed. Installing...")
            if not install_pre_commit():
                logger.error("Failed to install pre-commit")
                click.echo("Error: Failed to install pre-commit.")
                sys.exit(1)
            logger.info("pre-commit installed successfully")

    # Generate the hooks
    logger.info(f"Generating pre-commit hooks for {git_root}")
    click.echo(f"Generating pre-commit hooks for {git_root}...")
    start_time = time.time()
    result = generate_hooks(git_root, api_key, non_interactive, install)
    elapsed_time = time.time() - start_time
    logger.debug(f"Hook generation completed in {elapsed_time:.2f} seconds")

    if result["success"]:
        logger.info(f"Successfully generated pre-commit hooks at {result['config_path']}")
        click.echo(f"Successfully generated pre-commit hooks at {result['config_path']}.")
        if install:
            logger.info("Hooks installed successfully")
            click.echo("Hooks installed successfully.")
    else:
        error_msg = result.get('error', 'Unknown error')
        logger.error(f"Failed to generate hooks: {error_msg}")
        click.echo(f"Error: {error_msg}.")
        sys.exit(1)

    logger.info("Pre-commit hook generation command completed successfully")


@cli.command()
@click.option(
    "--repo-path",
    "-p",
    default=".",
    help="Path to the repository root. Defaults to current directory.",
)
def check_docs(repo_path: str = ".") -> None:
    """Check if documentation files are up-to-date."""
    from ai_hooks.utils import check_doc_freshness

    # Check if the path is a git repository
    if not is_git_repository(repo_path):
        click.echo(f"Error: {repo_path} is not a git repository.")
        sys.exit(1)

    # Get the repository root
    git_root = get_git_root(repo_path)
    if not git_root:
        click.echo(f"Error: Could not determine git repository root from {repo_path}.")
        sys.exit(1)

    # Check documentation freshness
    outdated_docs = check_doc_freshness(git_root)
    if outdated_docs:
        click.echo("The following documentation files may be outdated:")
        for doc in outdated_docs:
            click.echo(f"  - {doc}")
        sys.exit(1)
    else:
        click.echo("All documentation files are up-to-date.")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
