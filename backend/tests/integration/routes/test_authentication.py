from datetime import datetime
from time import sleep

from backend.app.schemas.user import User

# from backend.app.schemas.user import Create_user
from backend.tests.integration.base import BaseTest


class TestAuthentication(BaseTest):
    """Test class to test authentication routes."""

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

        user = User(**user)
        self.create_user(user=user)

        credentials = {
            "email": owner_email,
            "password": "password",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/authentication", json=credentials
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

        user = User(**user)
        self.create_user(user=user)

        credentials = {
            "email": "other_user",
            "password": "password",
        }

        # EXERCISE
        response = self.app_client.post(
            "/api/v1/authentication", json=credentials
        )

        # ASSERT
        # TODO - Assert text MESSAGE
        assert response.status_code == 404
        assert (
            response.text
            == '{"detail":{"type":"not_found","description":"The server can not find the requested resource.","detail":"User not found"}}'  # noqa: E501
        )

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

        user = User(**user)
        self.create_user(user=user)

        header = self.get_header(user_email, ["free"])
        token = header.get("Authorization").split(" ")[1]

        # EXERCISE
        sleep(2)
        response_renew = self.app_client.get(
            "/api/v1/authentication/renew", headers=header
        )

        # ASSERT
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

        user = User(**user)
        self.create_user(user=user)

        header = self.get_header(user_email, ["free"])
        token = header.get("Authorization").split(" ")[1]

        # EXERCISE

        token = token + "2"

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response_renew = self.app_client.get(
            "/api/v1/authentication/renew", headers=request_headers
        )

        # ASSERT
        assert response_renew.status_code == 401
        assert (
            response_renew.text
            == '{"detail":"Invalid Token Signature verification failed."}'
        )
