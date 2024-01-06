from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from backend.app.schemas.passwords import (
    PasswordHeader,
    PasswordList,
    PasswordStaging,
)
from backend.app.schemas.user import User

# from backend.app.schemas.user import Create_user
from backend.tests.integration.base import BaseTest
from backend.tests.integration.helper import generate_jwt_token


class TestUser(BaseTest):
    """Test class to test event service."""

    @patch("backend.app.events.email.EmailEvent.send_email")
    def test_create_user__send_valid_data__expect_created_user_in_database(  # noqa: E501
        self, email_send_mock: Mock
    ) -> None:
        """Test to send new user."""
        # FIXTURE
        owner_email = "usuario-teste@teste.com"
        user = {
            "email": owner_email,
            "password": "123456",
            "name": "Teste",
        }

        email_send_mock.return_value = None

        expected_user = {
            "email": owner_email,
            "name": "Teste",
            "roles": ["free"],
            "verificated": False,
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user",
            json=user,
        )

        # ASSERT
        assert response.status_code == 201
        assert response.json() == expected_user

    @patch("backend.app.events.email.EmailEvent.send_email")
    def test_create_user__send_invalid_data__expect_dont_create_user_in_database(  # noqa: E501
        self, email_send_mock: Mock
    ) -> None:
        """Test to send new user when user no send valid inputs."""
        # FIXTURE
        owner_email = "usuario-teste@teste.com"

        token = generate_jwt_token(owner_email)
        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        user = {
            "email": owner_email,
            "name": "Teste",
        }

        email_send_mock.return_value = None

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user",
            json=user,
            headers=request_headers,
        )

        # ASSERT
        assert response.status_code == 422

    @patch("backend.app.events.email.EmailEvent.send_email")
    def test_forgot_password__send_existing_email_and_after_time__expect_code_sended(  # noqa: E501
        self, email_send_mock: Mock
    ):
        """Test forgot password."""
        # FIXTURE
        user_email = "email-test@rmail.com"
        email_send_mock.return_value = None

        time_now = datetime.now()
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "123-456",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        body = {"email": user_email, "password": "other-password"}

        time_less = (datetime.utcnow() + timedelta(minutes=28)).isoformat()
        time_more = (datetime.utcnow() + timedelta(minutes=32)).isoformat()

        # EXERCISE

        response = self.app_client.post(
            "/api/v1/user/forgot-password",
            json=body,
        )

        # ASSERT
        content = response.json()

        assert response.status_code == 200
        assert content["id"] == user_email
        assert (
            content["valid_until"] > time_less
            and content["valid_until"] < time_more
        )

    @patch("backend.app.events.email.EmailEvent.send_email")
    def test_forgot_password__send_existing_email_and_before_time__expect_error(  # noqa: E501
        self, email_send_mock: Mock
    ):
        """Test forgot password."""
        # FIXTURE
        user_email = "email-test@rmail.com"
        email_send_mock.return_value = None

        time_now = datetime.now()
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "123-456",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        password_stg = PasswordStaging(
            code="123-457",
            id=user_email,
            password="--password--",
            valid_until=datetime.utcnow() + timedelta(minutes=30),
        )

        password_stg = self.create_database_doc.create_password_staging(
            password_stg
        )

        body = {"email": user_email, "password": "other-password"}

        # EXERCISE

        response = self.app_client.post(
            "/api/v1/user/forgot-password",
            json=body,
        )

        # ASSERT
        assert response.status_code == 400
        assert (
            response.json()["detail"]["detail"] == "Password already requested"
        )

    @patch("backend.app.events.email.EmailEvent.send_email")
    def test_forgot_password__send_password_already_exist_in_database__expect_error(  # noqa: E501
        self, email_send_mock: Mock
    ):
        """Test forgot password."""
        # FIXTURE
        user_email = "email-test@rmail.com"
        email_send_mock.return_value = None

        time_now = datetime.now()
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "123-456",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        equal_password = "other-password"

        password_header = PasswordHeader(
            created_at=time_now,
            password=equal_password,
        )

        password_list = PasswordList(
            id=user_email, passwords=[password_header]
        )

        password_list = self.create_database_doc.create_password_list(
            password_list
        )

        body = {"email": user_email, "password": equal_password}

        # EXERCISE

        response = self.app_client.post(
            "/api/v1/user/forgot-password",
            json=body,
        )

        # ASSERT
        assert (
            response.status_code == 409
        )  # épra dar erro porque nao faz o que tem que fazer
        assert (
            response.json()["detail"]["description"]
            == "The data already exist."
        )
