import logging
import os

import pytest


@pytest.fixture(autouse=True)
def reset_environment_variables():
    """Reset environment variables before each test."""
    original_environ = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(original_environ)


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    # Store original loggers and handlers
    root_logger = logging.getLogger()
    original_level = root_logger.level
    original_handlers = list(root_logger.handlers)

    yield

    # Restore original logging configuration
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    for handler in original_handlers:
        root_logger.addHandler(handler)

    root_logger.setLevel(original_level)


@pytest.fixture
def valid_api_key():
    """Return a valid API key format."""
    return "sk-abcdefghijklmnopqrstuvwxyz1234"
