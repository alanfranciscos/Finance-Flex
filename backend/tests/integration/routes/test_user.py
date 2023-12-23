# from datetime import datetime
from datetime import datetime
from time import sleep
from unittest.mock import Mock, patch

from backend.app.schemas.users.user import Create_user

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

    def test_authenticate_user__send_valid_data__expect_token(  # noqa: E501
        self,
    ) -> None:
        """Test to authenticate user."""
        # FIXTURE
        owner_email = "usuario-teste@teste.com"

        time_now = datetime.now()

        user = {
            "id": owner_email,
            "email": owner_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "12-34",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = Create_user(**user)
        self.create_user(user=user)

        credentials = {
            "email": owner_email,
            "password": "password",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/authenticate", json=credentials
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json() == {"message": "Authenticated"}
        assert response.cookies["access_token"]

    def test_authenticate_user__invalid_data__expect_error(  # noqa: E501
        self,
    ) -> None:
        """Test to authenticate user."""
        # FIXTURE
        user_email = "usuario-teste@teste.com"

        time_now = datetime.now()

        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "12-34",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = Create_user(**user)
        self.create_user(user=user)

        credentials = {
            "email": "other_user",
            "password": "password",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/user/authenticate", json=credentials
        )

        # ASSERT
        assert response.status_code == 404

    def test_renew_token__send_valid_token__expect_new_token(  # noqa: E501
        self,
    ) -> None:
        """Test to renew token."""
        # FIXTURE
        user_email = "usuario-teste@teste.com"

        time_now = datetime.now()

        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "12-34",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = Create_user(**user)
        self.create_user(user=user)

        credentials = {
            "email": user_email,
            "password": "password",
        }

        # EXERCISE
        response_authentice = self.app_client.post(
            "/api/v1/user/authenticate", json=credentials
        )

        token = response_authentice.cookies["access_token"]

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        sleep(1)

        response_renew = self.app_client.get(
            "/api/v1/user/authenticate/renew", headers=request_headers
        )

        # ASSERT
        assert response_authentice.status_code == 200
        assert response_authentice.json() == {"message": "Authenticated"}
        assert response_authentice.cookies["access_token"]
        assert response_renew.status_code == 200
        assert response_renew.json() == {"message": "Authenticated"}
        assert response_renew.cookies["access_token"]
        assert response_renew.cookies["access_token"] != token

    def test_renew_token__send_invalid_token__expect_error(  # noqa: E501
        self,
    ) -> None:
        """Test to renew token."""
        # FIXTURE
        user_email = "usuario-teste@teste.com"

        time_now = datetime.now()

        user = {
            "id": user_email,
            "email": user_email,
            "name": "Teste",
            "roles": ["free"],
            "password": "password",
            "verification": {
                "verified": True,
                "verification_code": "12-34",
                "valid_until": "2021-01-01T00:00:00",
            },
            "created_at": time_now,
            "updated_at": time_now,
        }

        user = Create_user(**user)
        self.create_user(user=user)

        credentials = {
            "email": user_email,
            "password": "password",
        }

        # EXERCISE
        response_authentice = self.app_client.post(
            "/api/v1/user/authenticate", json=credentials
        )

        token = response_authentice.cookies["access_token"] + "2"

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response_renew = self.app_client.get(
            "/api/v1/user/authenticate/renew", headers=request_headers
        )

        # ASSERT
        assert response_authentice.status_code == 200
        assert response_authentice.json() == {"message": "Authenticated"}
        assert response_authentice.cookies["access_token"]
        assert response_renew.status_code == 401
