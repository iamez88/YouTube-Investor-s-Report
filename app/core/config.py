from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "YouTube Summarizer API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API for summarizing YouTube videos."

    YOUTUBE_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

print(f"LOG_LEVEL is set to: {settings.LOG_LEVEL}")
