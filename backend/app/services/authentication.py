from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt

from app.config.settings import get_settings
from app.repositories.cookie import CookieRepository
from app.schemas.cookies import Cookie
from app.services.user import UserService
from app.utils import api_errors

_settings = get_settings()


class AuthenticationService:
    def __init__(
        self,
        user_service: UserService,
        cookie_repository: CookieRepository,
    ):
        """Init."""
        self._user_service = user_service
        self._cookie_repository = cookie_repository

    def _create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        """Function to create access token."""
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            _settings.JWT_SECRET_KEY,
            algorithm=_settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def _generate_token(self, email: str, roles: list[str]):
        """Generate token."""
        access_token_expires = timedelta(
            minutes=_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self._create_access_token(
            data={"user": email, "roles": roles},
            expires_delta=access_token_expires,
        )

        cookie = self._cookie_repository.Save(
            Cookie(
                id=email,
                token=access_token,
            )
        )
        if not cookie:
            raise HTTPException(
                status_code=500, detail="Error saving cookie in database"
            )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def authenticate(self, email: str, password: str) -> dict:
        """Authenticate user."""
        user = self._user_service.get(email)

        if not user:
            api_errors.raise_error_response(
                api_errors.NotFound,
                detail="User not found",
            )

        if not user.verification.verified:
            raise HTTPException(status_code=401, detail="User not verified")

        if not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Incorrect password")
        token = self._generate_token(email=email, roles=user.roles)
        return token

    def renew_token(self, token: str) -> dict:
        """Authenticate user."""
        try:
            payload = jwt.decode(
                token,
                _settings.JWT_SECRET_KEY,
                algorithms=[_settings.JWT_ALGORITHM],
            )
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Token {e}")

        email = payload.get("user")

        user = self._user_service.get(email)

        token = self._generate_token(email=email, roles=user.roles)

        return token
