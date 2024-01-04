from unittest.mock import Mock, patch

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
