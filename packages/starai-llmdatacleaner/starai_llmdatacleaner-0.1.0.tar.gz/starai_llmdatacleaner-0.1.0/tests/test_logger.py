import logging

from llmdatacleaner._utils.logger import (
    get_logger,
    set_logging_level,
)


def test_get_logger_default_level(reset_logging):
    """Test that get_logger returns a logger with the default level."""
    logger = get_logger("test_logger")
    assert logger.name == "test_logger"
    # The logger itself should inherit from the parent
    assert logger.level == 0


def test_get_logger_custom_level(reset_logging):
    """Test that get_logger sets the custom level when provided."""
    logger = get_logger("test_logger", level="DEBUG")
    assert logger.level == logging.DEBUG

    # Test with int level
    logger = get_logger("test_logger_int", level=logging.INFO)
    assert logger.level == logging.INFO


def test_set_logging_level_with_string(reset_logging):
    """Test setting the logging level with a string."""
    root_logger = logging.getLogger("llmdatacleaner")

    # Set to DEBUG level
    set_logging_level("DEBUG")
    assert root_logger.level == logging.DEBUG

    # Set to INFO level
    set_logging_level("INFO")
    assert root_logger.level == logging.INFO


def test_set_logging_level_with_int(reset_logging):
    """Test setting the logging level with an integer."""
    root_logger = logging.getLogger("llmdatacleaner")

    # Set to DEBUG level
    set_logging_level(logging.DEBUG)
    assert root_logger.level == logging.DEBUG

    # Set to INFO level
    set_logging_level(logging.INFO)
    assert root_logger.level == logging.INFO
