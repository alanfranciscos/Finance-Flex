from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from backend.app.schemas.user import UserInput
from backend.app.services.user import UserService


class TestUser:
    """Test class to test event service."""

    def test_validate_create_user_input__valid_email__expect_sucsecc(  # noqa: E501
        self,
    ) -> None:
        """Test to validate user input."""
        # FIXTURE
        email = "emailteste@teste.com"

        user_input = UserInput(
            email=email,
            password="password",
            name="name",
        )

        user_repository = Mock()
        user_repository.get_by_id.return_value = None

        user_sevice = UserService(
            user_repository=user_repository,
        )

        # EXERCISE
        user_sevice.validate_create_user_input(
            user_input=user_input,
        )

    def test_validate_create_user_input__invalid_email__expect_raise_error(  # noqa: E501
        self,
    ) -> None:
        """Test to validate user input."""
        with pytest.raises(HTTPException):
            # FIXTURE
            email = "emailteste.com"

            user_input = UserInput(
                email=email,
                password="password",
                name="name",
            )

            user_repository = Mock()
            user_repository.get_by_id.return_value = None

            user_sevice = UserService(
                user_repository=user_repository,
            )

            # EXERCISE
            user_sevice.validate_create_user_input(
                user_input=user_input,
            )

    def test_generate_verification_code__generate_verification_code__expect_verification_code(  # noqa: E501
        self,
    ) -> None:
        """Test to validate user input."""
        # FIXTURE
        user_sevice = UserService(
            user_repository=Mock(),
        )

        # EXERCISE
        code = user_sevice.generate_verification_code()

        # ASSERT
        assert code
        assert len(code) == 7
