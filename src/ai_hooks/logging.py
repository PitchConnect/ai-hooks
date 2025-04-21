"""Logging configuration for the AI Hooks."""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Optional, Union

# Define log levels with more descriptive names
TRACE = 5  # More detailed than DEBUG
logging.addLevelName(TRACE, "TRACE")


def trace(
    self: logging.Logger, message: object, *args: Any, **kwargs: Any
) -> None:
    """Log a message with TRACE level."""
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


# Add trace method to Logger class
# Using type ignore to tell mypy that we're modifying the Logger class
setattr(logging.Logger, 'trace', trace)  # type: ignore


class LogFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""

    COLORS = {
        "TRACE": "\033[35m",     # Magenta
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red background
        "RESET": "\033[0m",      # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors for console output."""
        log_message = super().format(record)
        # Only use colors when outputting to a terminal
        if sys.stdout.isatty():
            level_name = record.levelname
            if level_name in self.COLORS:
                color = self.COLORS[level_name]
                reset = self.COLORS['RESET']
                log_message = f"{color}{log_message}{reset}"
        return log_message


def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_to_console: bool = True,
) -> logging.Logger:
    """Set up logging for the application.

    Args:
        level: The logging level. Defaults to INFO.
        log_file: Path to the log file. If None, logs will only be output to console.
        log_to_console: Whether to output logs to console. Defaults to True.

    Returns:
        The configured logger.
    """
    # Convert string level to int if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger("ai_hooks")
    logger.setLevel(level)
    logger.handlers = []  # Remove any existing handlers

    # Create formatters
    console_formatter = LogFormatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s "
        "(%(filename)s:%(lineno)d): "
        "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Add console handler if requested
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Add file handler if log file is specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger with the specified name.

    If the logger hasn't been set up yet, it will be set up with default settings.

    Args:
        name: The name of the logger. If None, the root logger will be returned.

    Returns:
        The logger.
    """
    if name:
        logger_name = f"ai_hooks.{name}"
    else:
        logger_name = "ai_hooks"

    logger = logging.getLogger(logger_name)

    # If the root logger doesn't have handlers, set up logging with defaults
    root_logger = logging.getLogger("ai_hooks")
    if not root_logger.handlers:
        # Get log level from environment variable or use INFO as default
        log_level = os.environ.get("AI_HOOKS_LOG_LEVEL", "INFO")

        # Get log file from environment variable or use None as default
        log_file = os.environ.get("AI_HOOKS_LOG_FILE")
        setup_logging(level=log_level, log_file=log_file)

    return logger
