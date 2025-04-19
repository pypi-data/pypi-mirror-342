import logging
from logging import Logger
from typing import Optional, Union

# Default to WARNING level (no INFO logs)
DEFAULT_LOGGING_LEVEL = logging.WARNING


def set_logging_level(level: Union[int, str]) -> None:
    """
    Set the global logging level for the LLMDataCleaner package.

    Args:
        level: Logging level (either as int or string like 'INFO', 'DEBUG', etc.)
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())

    # Set the root logger level
    logging.getLogger("llmdatacleaner").setLevel(level)

    # Update handlers on the root logger
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)


def get_logger(name: str, level: Optional[Union[int, str]] = None) -> Logger:
    """
    Logger to log information on console.

    Args:
        name: Logger name
        level: Optional specific level for this logger
              (overrides the global setting)

    Returns:
        Configured logger instance
    """
    # Only configure root logger once
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=DEFAULT_LOGGING_LEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # # Get logger with the package prefix
    # if not name.startswith("llmdatacleaner"):
    #     logger_name = f"llmdatacleaner.{name}" if not name.startswith("_") else name
    # else:
    #     logger_name = name

    logger = logging.getLogger(name)

    # Apply specific level if provided
    if level is not None:
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        logger.setLevel(level)

    return logger
