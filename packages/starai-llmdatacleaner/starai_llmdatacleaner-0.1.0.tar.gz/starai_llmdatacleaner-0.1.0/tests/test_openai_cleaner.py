from unittest.mock import AsyncMock, Mock, patch

import pytest

from llmdatacleaner.openai_cleaner import ModelName, OpenAIDataCleaner


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client"""
    with patch("openai.OpenAI") as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_async_openai_client():
    """Create a mock Async OpenAI client"""
    with patch("openai.AsyncOpenAI") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def sample_data_cleaner(valid_api_key, mock_openai_client, mock_async_openai_client):
    """Create a sample OpenAIDataCleaner instance"""
    return OpenAIDataCleaner(
        openai_api_key="test_api_key",
        data_cleaning_prompt="Clean this data",
        output_format={"format": {"type": "json", "schema": {"type": "object"}}},
    )


def test_init_with_default_values(valid_api_key, mock_openai_client):
    """Test initialization with default values"""
    cleaner = OpenAIDataCleaner(
        data_cleaning_prompt="Clean this data",
        output_format={"format": {"type": "json"}},
        openai_api_key="test_api_key",
    )
    assert cleaner.data_cleaning_prompt == "Clean this data"
    assert cleaner.model_name == ModelName.GPT4O_MINI.value
    assert cleaner.system_prompt == OpenAIDataCleaner.DEFAULT_SYSTEM_PROMPT


def test_init_with_custom_values(valid_api_key, mock_openai_client):
    """Test initialization with custom values"""
    cleaner = OpenAIDataCleaner(
        openai_api_key="test_api_key",
        data_cleaning_prompt="Custom cleaning prompt",
        output_format={"format": {"type": "json"}},
        model_name=ModelName.GPT4O.value,
        system_prompt="Custom system prompt",
        verbose=True,
    )
    assert cleaner.data_cleaning_prompt == "Custom cleaning prompt"
    assert cleaner.model_name == ModelName.GPT4O.value
    assert cleaner.system_prompt == "Custom system prompt"


def test_property_setters(sample_data_cleaner):
    """Test property setters"""
    # Test model_name setter
    sample_data_cleaner.model_name = ModelName.GPT41.value
    assert sample_data_cleaner.model_name == ModelName.GPT41.value

    # Test system_prompt setter
    sample_data_cleaner.system_prompt = "New system prompt"
    assert sample_data_cleaner.system_prompt == "New system prompt"

    # Test data_cleaning_prompt setter
    sample_data_cleaner.data_cleaning_prompt = "New cleaning prompt"
    assert sample_data_cleaner.data_cleaning_prompt == "New cleaning prompt"

    # Test output_format setter
    new_format = {"format": {"type": "json", "schema": {"type": "array"}}}
    sample_data_cleaner.output_format = new_format
    assert sample_data_cleaner.output_format == new_format


def test_invalid_property_values(sample_data_cleaner):
    """Test invalid property values raise appropriate errors"""
    # Test invalid model name
    with pytest.raises(ValueError):
        sample_data_cleaner.model_name = "invalid-model"

    # Test empty system prompt
    with pytest.raises(ValueError):
        sample_data_cleaner.system_prompt = ""

    # Test empty data cleaning prompt
    with pytest.raises(ValueError):
        sample_data_cleaner.data_cleaning_prompt = ""

    # Test invalid output format (not a dict)
    with pytest.raises(ValueError):
        sample_data_cleaner.output_format = "not-a-dict"

    # Test invalid output format (missing format key)
    with pytest.raises(ValueError):
        sample_data_cleaner.output_format = {"schema": {"type": "object"}}


def test_prepare_request(sample_data_cleaner):
    """Test _prepare_request method"""
    request = sample_data_cleaner._prepare_request("Test data")

    assert request["model"] == ModelName.GPT4O_MINI.value
    assert request["input"][0]["role"] == "system"
    assert request["input"][0]["content"] == OpenAIDataCleaner.DEFAULT_SYSTEM_PROMPT
    assert request["input"][1]["role"] == "user"
    assert "Test data" in request["input"][1]["content"]
    assert request["text"] == {"format": {"type": "json", "schema": {"type": "object"}}}


def test_invoke_success(sample_data_cleaner, mock_openai_client):
    """Test successful invocation"""
    # Mock a successful API response
    mock_response = Mock()
    mock_response.output_text = '{"cleaned": true}'
    mock_openai_client.responses.create.return_value = mock_response

    result = sample_data_cleaner.invoke("Test data")

    assert result["status"] == "success"
    assert result["original"] == "Test data"
    assert result["cleaned"] == {"cleaned": True}
    assert result["error"] is None


def test_invoke_json_error(sample_data_cleaner, mock_openai_client):
    """Test handling invalid JSON in response"""
    # Mock an API response with invalid JSON
    mock_response = Mock()
    mock_response.output_text = "Invalid JSON"
    mock_openai_client.responses.create.return_value = mock_response

    result = sample_data_cleaner.invoke("Test data")

    assert result["status"] == "success"  # We still consider this a success
    assert result["original"] == "Test data"
    assert result["cleaned"] == "Invalid JSON"  # Raw text used as fallback
    assert result["error"] is None


def test_invoke_api_error(sample_data_cleaner, mock_openai_client):
    """Test API error handling"""
    # Mock an API error
    mock_openai_client.responses.create.side_effect = Exception("API Error")

    result = sample_data_cleaner.invoke("Test data")

    assert result["status"] == "error"
    assert result["original"] == "Test data"
    assert result["cleaned"] is None
    assert "API Error" in result["error"]


@pytest.mark.asyncio
async def test_ainvoke_success(sample_data_cleaner, mock_async_openai_client):
    """Test successful async invocation"""
    # Mock a successful async API response
    mock_response = Mock()
    mock_response.output_text = '{"cleaned": true}'
    mock_async_openai_client.responses.create.return_value = mock_response

    result = await sample_data_cleaner.ainvoke("Test data")

    assert result["status"] == "success"
    assert result["original"] == "Test data"
    assert result["cleaned"] == {"cleaned": True}
    assert result["error"] is None


@pytest.mark.asyncio
async def test_ainvoke_error(sample_data_cleaner, mock_async_openai_client):
    """Test async API error handling"""
    # Mock an async API error
    mock_async_openai_client.responses.create.side_effect = Exception("Async API Error")

    result = await sample_data_cleaner.ainvoke("Test data")

    assert result["status"] == "error"
    assert result["original"] == "Test data"
    assert result["cleaned"] is None
    assert "Async API Error" in result["error"]


def test_set_verbose():
    """Test the static set_verbose method"""
    with patch("llmdatacleaner.openai_cleaner.set_logging_level") as mock_set_level:
        OpenAIDataCleaner.set_verbose(True)
        mock_set_level.assert_called_once_with("INFO")

        mock_set_level.reset_mock()

        OpenAIDataCleaner.set_verbose(False)
        mock_set_level.assert_called_once_with("WARNING")
