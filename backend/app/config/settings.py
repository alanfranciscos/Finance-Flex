import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Global settings."""

    API_V1: str = "/api/v1"
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_SECRET_KEY: str = os.getenv("JWT_AUDIENCE")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_PORT: int = os.getenv("EMAIL_PORT")


def get_settings() -> Settings:
    """Get instance of settings."""
    return Settings()
