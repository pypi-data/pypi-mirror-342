import json
from enum import Enum
from typing import Any, Dict, Literal, Optional, TypedDict

import openai

from ._api_validation import _get_openai_api
from ._utils.logger import get_logger, set_logging_level

logger = get_logger(__name__)


class CleaningResult(TypedDict):
    """Type definition for a cleaning result"""

    original: Any
    cleaned: Any
    status: Literal["success", "error"]
    error: Optional[str]


class ModelName(str, Enum):
    """Supported OpenAI model names"""

    GPT4O_MINI = "gpt-4o-mini"
    GPT4O = "gpt-4o"
    GPT41 = "gpt-4.1"
    GPT41_MINI = "gpt-4.1-mini"


class OpenAIDataCleaner:
    DEFAULT_MODEL: str = ModelName.GPT4O_MINI.value
    DEFAULT_MAX_WORKERS: int = 5
    DEFAULT_SYSTEM_PROMPT: str = "You are a helpful data cleaning assistant."

    def __init__(
        self,
        data_cleaning_prompt: str,
        output_format: Dict[str, Dict],
        openai_api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
        verbose: bool = False,
    ):
        self.data_cleaning_prompt = data_cleaning_prompt
        self.output_format = output_format
        self.model_name = model_name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self._api_key = _get_openai_api(openai_api_key)
        self._client = openai.OpenAI(api_key=self._api_key)
        self._async_client = openai.AsyncOpenAI(api_key=self._api_key)

        # Set verbosity
        if verbose:
            set_logging_level("INFO")

        logger.info(f"Initialized OpenAIDataCleaner with model {self._model_name}")

    @staticmethod
    def set_verbose(verbose: bool = True) -> None:
        """
        Set the verbosity of the logger.

        Args:
            verbose: If True, set logging to INFO level, otherwise WARNING
        """
        level = "INFO" if verbose else "WARNING"
        set_logging_level(level)

    @property
    def data_cleaning_prompt(self) -> str:
        return self._data_cleaning_prompt

    @data_cleaning_prompt.setter
    def data_cleaning_prompt(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Data cleaning prompt cannot be empty")
        self._data_cleaning_prompt = value
        logger.info("Set data cleaning prompt")

    @property
    def model_name(self) -> str:
        return self._model_name

    @model_name.setter
    def model_name(self, value: str) -> None:
        valid_models = [model.value for model in ModelName]
        if value not in valid_models:
            raise ValueError(
                f"Model name '{value}' may not be valid. "
                f"Recommended models: {', '.join(valid_models)}"
            )
        self._model_name = value
        logger.info(f"Model name set to {self._model_name}")

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("System prompt cannot be empty")
        self._system_prompt = value
        logger.info("Set system prompt")

    @property
    def output_format(self) -> Dict[str, Dict]:
        return self._output_format

    @output_format.setter
    def output_format(self, value: Dict[str, Dict]):
        if not isinstance(value, dict):
            raise ValueError("Output format must be a dictionary")
        if "format" not in value:
            raise ValueError("Output format must contain a 'format' key")
        self._output_format = value
        logger.info(f"Set output format to: {value}")

    def _prepare_request(self, item: Any) -> Dict:
        """
        Prepare the request parameters for OpenAI API.

        Args:
            item: The data item to clean

        Returns:
            Dictionary of request parameters
        """
        full_prompt = f"{self._data_cleaning_prompt}\nData: {str(item)}"
        return {
            "model": self._model_name,
            "input": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": full_prompt},
            ],
            "text": self._output_format,
        }

    def _process_response(self, response, item: Any) -> CleaningResult:
        """
        Process the API response and create a CleaningResult.

        Args:
            response: Response from OpenAI API
            item: Original data item

        Returns:
            CleaningResult with processed data
        """
        try:
            cleaned_data = json.loads(response.output_text)
        except json.JSONDecodeError as json_err:
            logger.warning(f"Failed to parse JSON response: {json_err}")
            # Fallback to using the raw text
            cleaned_data = response.output_text

        return {
            "original": item,
            "cleaned": cleaned_data,
            "status": "success",
            "error": None,
        }

    def _handle_error(self, error: Exception, item: Any) -> CleaningResult:
        """
        Create a CleaningResult for a failed request.

        Args:
            error: The exception that occurred
            item: Original data item

        Returns:
            CleaningResult with error information
        """
        logger.error(f"Error cleaning item: {str(error)}")
        return {
            "original": item,
            "cleaned": None,
            "status": "error",
            "error": str(error),
        }

    def invoke(self, item: Any) -> CleaningResult:
        """
        Clean a single data item using the OpenAI model.

        Args:
            item: The data item to clean

        Returns:
            A dictionary containing the original and cleaned item
        """
        try:
            request_params = self._prepare_request(item)
            response = self._client.responses.create(**request_params)
            return self._process_response(response, item)
        except Exception as e:
            return self._handle_error(e, item)

    async def ainvoke(self, item: Any) -> CleaningResult:
        """
        Asynchronously clean a single data item using the OpenAI model.

        Args:
            item: The data item to clean

        Returns:
            A dictionary containing the original and cleaned item
        """
        try:
            request_params = self._prepare_request(item)
            response = await self._async_client.responses.create(**request_params)
            return self._process_response(response, item)
        except Exception as e:
            return self._handle_error(e, item)
