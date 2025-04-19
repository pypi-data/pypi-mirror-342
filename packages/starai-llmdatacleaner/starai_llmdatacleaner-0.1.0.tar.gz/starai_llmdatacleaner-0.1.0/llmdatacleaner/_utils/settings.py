from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # openai api key
    openai_key: Optional[str] = Field(default=None, validation_alias="OPENAI_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",  # fallback file
        env_file_encoding="utf-8",
    )
