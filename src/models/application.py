"""Application data models."""
from pydantic import Field, HttpUrl

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(env_ignore_empty=True)
    # collibra_base64_encoded_credentials: str = Field(min_length=1, repr=False)
    # collibra_url: HttpUrl
