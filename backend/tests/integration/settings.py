import os

from dotenv import load_dotenv

from app.config.settings import Settings


def get_settings() -> Settings:
    """Get current settings for test."""
    if os.path.exists(os.path.join(os.getcwd(), ".env-tests")):
        os.environ["APP_PATH"] = os.getcwd()
        load_dotenv(os.path.join(os.getcwd(), ".env-tests"), override=True)

    _settings = Settings()

    _settings.API_V1: str = "/api/v1"
    _settings.MONGO_URI: str = os.getenv("MONGO_URI")
    _settings.MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")

    _settings.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    _settings.JWT_SECRET_KEY: str = os.getenv("JWT_AUDIENCE")
    _settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    _settings.EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    _settings.EMAIL_USER: str = os.getenv("EMAIL_USER")
    _settings.EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    _settings.EMAIL_PORT: int = os.getenv("EMAIL_PORT")
    return _settings
