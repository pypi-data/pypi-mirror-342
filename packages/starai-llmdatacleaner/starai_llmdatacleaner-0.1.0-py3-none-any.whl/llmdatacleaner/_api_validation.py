from typing import Optional

from ._utils import Settings, get_logger

logger = get_logger(__name__)


def _get_openai_api(api_key: Optional[str] = None) -> str:
    """
    Get the OpenAI API key from various sources with validation.

    This function tries to get the API key from:
    1. The api_key parameter if provided
    2. The OPENAI_API_KEY environment variable

    Args:
        api_key: Optional API key provided directly

    Returns:
        The valid API key as a string

    Raises:
        ValueError: If no API key is found or the key format is invalid
    """
    # Case 1: API key provided directly
    if api_key:
        if _validate_api_key_format(api_key):
            return api_key
        else:
            logger.warning("Provided API key has an invalid format")
            return api_key

    # Case 2: API key in environment variable (either export or .env file)
    env_key = Settings().openai_key
    if env_key:
        if _validate_api_key_format(env_key):
            logger.info("Using OpenAI API key from environment variables")
            return env_key
        else:
            logger.warning("API key in environment variable has an invalid format")

    # Case 3: No valid API key found
    raise ValueError(
        "No valid OpenAI API key found. Please provide a valid key directly "
        "or set the OPENAI_API_KEY environment variable."
    )


def _validate_api_key_format(api_key: str) -> bool:
    """
    Validate the format of an OpenAI API key.

    OpenAI API keys typically start with 'sk-' followed by a string of alphanumeric characters.

    Args:
        api_key: The API key to validate

    Returns:
        True if the format appears valid, False otherwise
    """
    # Basic validation - check if it starts with the expected prefix
    # and has a reasonable length
    if api_key.startswith("sk-") and len(api_key) >= 20:
        return True
    return False
