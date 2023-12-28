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
from backend.app.repositories.cookies import CookieRepository
from backend.app.repositories.users.password import PasswordsRepository
from backend.app.repositories.users.password_staging import (
    PsswordStagingRepository,
)
from backend.app.repositories.users.user import UserRepository
from backend.app.schemas.cookies import Cookie
from backend.app.schemas.users.password import PasswordStaging
from backend.app.schemas.users.user import (
    Create_user,
    User,
    UserInput,
    UserVerification,
)
from backend.app.utils import api_errors

_settings = get_settings()


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        cookie_repository: CookieRepository,
        password_repository: PasswordsRepository,
        password_staging_repository: PsswordStagingRepository,
    ) -> None:
        """init."""
        self._user_repository = user_repository
        self._cookie_repository = cookie_repository
        self._password_repository = password_repository
        self._password_staging_repository = password_staging_repository
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._emailEvent = EmailEvent()

    def get(self, email: str) -> User:
        """Get a user."""
        user = self._user_repository.get_by_id(email)
        return user

    def validate_create_user_input(self, user_input: UserInput) -> None:
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
        while i < 3:
            number = random.randint(0, 9)
            verification_code += str(number)
            i += 1

        verification_code += "-"

        i = 0
        while i < 3:
            number = random.randint(0, 9)
            verification_code += str(number)
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

        self._emailEvent.send_email(
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

    def generate_token(self, email: str, roles: list[str]):
        """Generate token."""
        access_token_expires = timedelta(
            minutes=_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.create_access_token(
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

    def _verify_password(self, old_password: str, new_password: str):
        if bcrypt.checkpw(
            old_password.encode("utf-8"),
            new_password.encode("utf-8"),
        ):
            raise HTTPException(
                status_code=401, detail="Password already used"
            )

    def request_forgot_password(
        self, id: str, password: str
    ) -> PasswordStaging:
        """Forgot password."""
        passwor_user = self._user_repository.get_password_from_user(id)

        password_hashed = self._pwd_context.hash(password)

        list_of_passwords = self._password_repository.get_passwords_from_user(
            id=id
        )
        self._verify_password(password, passwor_user)
        if list_of_passwords:
            for _password in list_of_passwords.passwords:
                self._verify_password(password, _password.password)

        code = self.generate_verification_code()
        create_password_staging = PasswordStaging(
            id=id,
            password=password_hashed,
            code=code,
            valid_until=datetime.utcnow() + timedelta(minutes=30),
        )
        create_password_staging = (
            self._password_staging_repository.save_password_staging(
                password_staging=create_password_staging
            )
        )

        self._emailEvent.send_email(
            boddy=f"Your verification code is: {code}",
            to=id,
            subject="Verification code - Forget password",
        )

        return create_password_staging
