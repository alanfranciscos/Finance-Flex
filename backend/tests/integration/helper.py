import importlib
import os
from datetime import datetime, timedelta
from typing import List

from dotenv.main import load_dotenv
from jose import jwt

import app.config.settings as settings


def set_envs_for_tests() -> None:
    """Set environment variables for test."""
    if os.path.exists(os.path.join(os.getcwd(), ".env-tests")):
        os.environ["APP_PATH"] = os.getcwd()
        load_dotenv(os.path.join(os.getcwd(), ".env-tests"), override=True)
        importlib.reload(settings)


def generate_jwt_token(
    user_email: str,
    roles: List[str] = [],
) -> str:
    """Generate jwt token."""

    data = {"user": user_email, "roles": roles}
    expires_delta = timedelta(
        minutes=settings.get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.get_settings().JWT_SECRET_KEY,
        algorithm=settings.get_settings().JWT_ALGORITHM,
    )

    return token
