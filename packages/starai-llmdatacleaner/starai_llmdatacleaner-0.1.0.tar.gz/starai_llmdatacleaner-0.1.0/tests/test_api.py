import os
from unittest.mock import patch

import pytest

from llmdatacleaner._api_validation import _get_openai_api, _validate_api_key_format
from llmdatacleaner._utils import Settings


def test_validate_api_key_format():
    """Test the API key format validation."""
    # Valid key
    assert _validate_api_key_format("sk-abcdefghijklmnopqrstuvwxyz1234") is True

    # Invalid keys
    assert _validate_api_key_format("not-a-valid-key") is False
    assert _validate_api_key_format("sk-tooshort") is False
    assert _validate_api_key_format("") is False


@patch.dict(os.environ, {}, clear=True)
def test_get_openai_api_with_direct_key():
    """Test getting API key when provided directly."""
    valid_key = "sk-abcdefghijklmnopqrstuvwxyz1234"
    assert _get_openai_api(valid_key) == valid_key


@patch.dict(os.environ, {"OPENAI_API_KEY": "sk-abcdefghijklmnopqrstuvwxyz1234"})
def test_get_openai_api_from_env():
    """Test getting API key from environment variable."""
    assert _get_openai_api() == "sk-abcdefghijklmnopqrstuvwxyz1234"


@patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"})
def test_get_openai_api_invalid_env():
    """Test with invalid environment API key."""
    with pytest.raises(ValueError):
        _get_openai_api()


@patch.dict(os.environ, {}, clear=True)
def test_get_openai_api_missing():
    """Test when no API key is provided."""
    with patch.object(Settings, "model_config", {"env_file": None}):
        with pytest.raises(ValueError):
            _get_openai_api()
