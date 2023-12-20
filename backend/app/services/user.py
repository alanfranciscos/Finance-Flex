"""User service"""
import random
import re
from datetime import datetime

from passlib.context import CryptContext

from backend.app.events.email import EmailEvent
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import Create_user, User, UserInput
from backend.app.utils import api_errors


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        """init."""
        self._user_repository = user_repository
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
        # TODO generate new code after 30m  if not verified user
        verification_code = self.generate_verification_code()
        time_now = str(datetime.now())

        user = Create_user(
            id=user_input.email,
            email=user_input.email,
            roles=["free"],
            password=password_hashed,
            verification={
                "verified": False,
                "verification_code": verification_code,
            },
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
