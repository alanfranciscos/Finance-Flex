"""Authentication service"""

from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from backend.app.config.settings import get_settings
from backend.app.repositories.authentication import AuthenticationRepository
from backend.app.services.user import UserService

settings = get_settings()


class AuthenticationService:
    def __init__(
        self,
        user_service: UserService,
        authentication_repository: AuthenticationRepository,
    ) -> None:
        """init."""
        self._user_service = user_service
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._authentication_repository = authentication_repository

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def authenticate(self, email: str, password: str):
        """Authenticate user."""
        self._user_service.get_by_id(email)

        user = self._authentication_repository.get_credentials(email)
        if not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.create_access_token(
            data={"user": email, "roles": user.roles},
            expires_delta=access_token_expires,
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
