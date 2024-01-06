import random
import re
from datetime import datetime, timedelta

import bcrypt
from passlib.context import CryptContext

from backend.app.events.email import EmailEvent
from backend.app.repositories.password_staging import PsswordStagingRepository
from backend.app.repositories.passwords import PasswordsRepository
from backend.app.repositories.users import UserRepository
from backend.app.schemas.passwords import (
    PasswordStaging,
    PasswordStagingValidate,
)
from backend.app.schemas.user import (
    User,
    UserInformations,
    UserInput,
    UserVerification,
)
from backend.app.utils import api_errors


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_repository: PasswordsRepository,
        password_staging_repository: PsswordStagingRepository,
    ):
        """Init."""
        self._user_repository = user_repository
        self._password_repository = password_repository
        self._password_staging_repository = password_staging_repository
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
    ) -> UserInformations:
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

        user = User(
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
        created_user = created_user.model_dump()
        created_user["verificated"] = created_user["verification"]["verified"]

        user_informations = UserInformations(**created_user)

        return user_informations

    def _verify_password(self, old_password: str, new_password: str):
        if bcrypt.checkpw(
            old_password.encode("utf-8"),
            new_password.encode("utf-8"),
        ):
            api_errors.raise_error_response(
                api_errors.DataAlreadyExists,
            )

    def request_forgot_password(
        self, id: str, password: str
    ) -> PasswordStagingValidate:
        """Forgot password."""
        user = self.get(id)
        password_user = user.password

        password_hashed = self._pwd_context.hash(password)

        list_of_passwords = self._password_repository.get_list(user=id)
        self._verify_password(password, password_user)
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
        password_staging_validate = (
            self._password_staging_repository.save_password_staging(
                password_staging=create_password_staging
            )
        )

        self._emailEvent.send_email(
            boddy=f"Your verification code is: {code}",
            to=id,
            subject="Verification code - Forget password",
        )

        return password_staging_validate
