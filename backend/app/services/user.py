"""User service"""
import random
import re
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.config.settings import get_settings
from backend.app.events.email import EmailEvent
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import (
    Create_user,
    User,
    UserInput,
    UserVerification,
)
from backend.app.utils import api_errors

_settings = get_settings()


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        """init."""
        self._user_repository = user_repository
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get(self, email: str) -> User:
        """Get a user."""
        user = self._user_repository.get_by_id(email)
        return user

    def validate_create_user_input(self, user_input: UserInput):
        """Validate user input."""

        if self.get(user_input.email):
            api_errors.raise_error_response(
                api_errors.ErrorResourceDataInvalid,
                detail="User already exists",
            )

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        _math_email = re.match(pattern, user_input.email) is not None

        if not _math_email:
            api_errors.raise_error_response(
                api_errors.ErrorResourceDataInvalid,
                detail="Invalid email",
            )

    def generate_verification_code(self) -> str:
        """Generate a verification code."""

        verification_code = ""
        i = 0
        while i < 2:
            verification_code += str(random.randint(1, 10))
            i += 1

        verification_code += "-"

        i = 0
        while i < 2:
            verification_code += str(random.randint(1, 10))
            i += 1
        return verification_code

    def create(
        self,
        user_input: UserInput,
    ) -> User:
        """Create a user."""
        self.validate_create_user_input(user_input=user_input)

        password_hashed = self._pwd_context.hash(user_input.password)

        verification_code = self.generate_verification_code()
        time_now = datetime.now()

        valid_until = datetime.now() + timedelta(minutes=30)

        verification = UserVerification(
            verified=False,
            verification_code=verification_code,
            valid_until=valid_until,
        )

        user = Create_user(
            id=user_input.email,
            name=user_input.name,
            email=user_input.email,
            roles=["free"],
            password=password_hashed,
            verification=verification,
            created_at=time_now,
            updated_at=time_now,
        )

        EmailEvent().send_email(
            boddy=f"Your verification code is: {verification_code}",
            to=user.email,
            subject="Verification code",
        )

        created_user = self._user_repository.create(user)
        return created_user

    def get_by_id(
        self,
        email: str,
    ) -> User:
        """Get a user by email."""

        user = self.get(email)

        if not user:
            api_errors.raise_error_response(
                api_errors.NotFound,
            )

        return user

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            _settings.JWT_SECRET_KEY,
            algorithm=_settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def generate_token(self, email: str, roles: list[str]):
        """Generate token."""
        access_token_expires = timedelta(
            minutes=_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.create_access_token(
            data={"user": email, "roles": roles},
            expires_delta=access_token_expires,
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def authenticate(self, email: str, password: str) -> dict:
        """Authenticate user."""
        self.get_by_id(email)

        user = self._user_repository.get_credentials(email)
        if not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Incorrect password")
        token = self.generate_token(email=email, roles=user.roles)
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

        self.get_by_id(email)
        user = self._user_repository.get_credentials(email)

        token = self.generate_token(email=email, roles=user.roles)

        return token
