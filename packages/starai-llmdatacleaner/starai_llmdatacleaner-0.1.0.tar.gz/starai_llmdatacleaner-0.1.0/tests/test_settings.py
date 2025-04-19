import os
from unittest.mock import patch

from llmdatacleaner._utils.settings import Settings


@patch.dict(os.environ, {}, clear=True)
def test_settings_default_values():
    with patch.object(Settings, "model_config", {"env_file": None}):
        settings = Settings()
        assert settings.openai_key is None


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
def test_settings_from_env_var():
    """Test that settings loads from environment variables."""
    settings = Settings()
    assert settings.openai_key == "test-api-key"


def test_env_file_config():
    """Test that settings has the correct env_file configuration."""
    assert Settings.model_config["env_file"] == ".env"
