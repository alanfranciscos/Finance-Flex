from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from app.schemas.passwords import (
    PasswordHeader,
    PasswordList,
    PasswordStaging,
)
from app.schemas.user import User

# from app.schemas.user import Create_user
from tests.integration.base import BaseTest
from tests.integration.helper import generate_jwt_token


class TestUser(BaseTest):
    """Test class to test event service."""

    @patch("app.events.email.EmailEvent.send_email")
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

    @patch("app.events.email.EmailEvent.send_email")
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

    @patch("app.events.email.EmailEvent.send_email")
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

    @patch("app.events.email.EmailEvent.send_email")
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

    @patch("app.events.email.EmailEvent.send_email")
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

    def test_code_validation__send_valid_code_firtst_validation__expect_true(
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": False,
                "verification_code": "585-858",
                "valid_until": time_now + timedelta(minutes=30),
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        body = {
            "email": user_email,
            "code": "585-858",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json() == "user verified"

    def test_code_validation__send_invalid_code_firtst_validation__expect_error(  # noqa: E501
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        valid_until = time_now + timedelta(minutes=30)
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": False,
                "verification_code": "585-858",
                "valid_until": valid_until,
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        body = {
            "email": user_email,
            "code": "999-999",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT

        assert response.status_code == 400
        assert (
            response.json()["detail"]["description"] == "The data is expired."
        )

    def test_code_validation__send_valid_code_staging_validation__expect_true(
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        valid_until = time_now + timedelta(minutes=30)
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "585-858",
                "valid_until": valid_until,
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        password_stg = PasswordStaging(
            code="605-506",
            id=user_email,
            password="--password--",
            valid_until=valid_until,
        )

        self.create_database_doc.create_password_staging(
            password_stg=password_stg
        )

        body = {
            "email": user_email,
            "code": "605-506",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT

        assert response.status_code == 200
        assert response.json() == "user verified"

    def test_code_validation__send_invalid_code_staging_validation__expect_error(  # noqa: E501
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        valid_until = time_now + timedelta(minutes=30)
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "585-858",
                "valid_until": valid_until,
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        password_stg = PasswordStaging(
            code="605-506",
            id=user_email,
            password="--password--",
            valid_until=valid_until,
        )

        self.create_database_doc.create_password_staging(
            password_stg=password_stg
        )

        body = {
            "email": user_email,
            "code": "999-999",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT

        assert response.status_code == 400
        assert (
            response.json()["detail"]["description"] == "The data is expired."
        )

    def test_code_validation__send_valid_code_first_validation_but_time_except___expect_true(  # noqa: E501
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        valid_until = time_now - timedelta(minutes=30)
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": False,
                "verification_code": "585-858",
                "valid_until": valid_until,
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        body = {
            "email": user_email,
            "code": "999-999",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT

        assert response.status_code == 400
        assert (
            response.json()["detail"]["description"] == "The data is expired."
        )

    def test_code_validation__send_valid_code_staging_validation_but_time_except___expect_true(  # noqa: E501
        self,
    ):
        """Test code validation."""
        # FIXTURE
        user_email = "email-teste@gmail.com"

        time_now = datetime.utcnow()
        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "585-858",
                "valid_until": time_now,
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = User(**user)
        self.create_database_doc.create_user(user=user)

        valid_until = time_now - timedelta(minutes=30)
        password_stg = PasswordStaging(
            code="605-506",
            id=user_email,
            password="--password--",
            valid_until=valid_until,
        )

        self.create_database_doc.create_password_staging(
            password_stg=password_stg
        )

        body = {
            "email": user_email,
            "code": "999-999",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/code-validation",
            json=body,
        )

        # ASSERT

        assert response.status_code == 400
        assert (
            response.json()["detail"]["description"] == "The data is expired."
        )
