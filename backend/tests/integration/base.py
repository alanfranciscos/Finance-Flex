from datetime import timezone
from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from backend.app.schemas.user import User
from backend.tests.integration.database import (
    get_database as get_database_tests,
)
from backend.tests.integration.helper import (
    generate_jwt_token,
    set_envs_for_tests,
)
from backend.tests.integration.settings import (
    get_settings as get_settings_tests,
)

DEFAULT_TIMEZONE = timezone.utc


class BaseTest:
    """Class that defines base test."""

    @classmethod
    def setup_class(cls) -> None:
        """Class setup.

        Setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        set_envs_for_tests()
        cls.settings = get_settings_tests()

        def _get_app() -> FastAPI:
            from backend.app.config.settings import get_settings
            from backend.app.dependencies.database import get_database
            from backend.app.main import app

            app.dependency_overrides[get_settings] = get_settings_tests
            app.dependency_overrides[get_database] = get_database_tests

            return app

        cls.app_client = TestClient(_get_app())

        cls.database = get_database_tests()
        cls.users_collection = cls.database.get_collection("users")

    def create_user(self, user: User) -> User:
        """Create user in database."""
        user = user.model_dump()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user["password"] = pwd_context.hash(user["password"])

        user["_id"] = user["id"]
        user.pop("id")
        self.users_collection.insert_one(user)

        doc = self.users_collection.find_one({"_id": user["_id"]})

        user = {k: v for k, v in doc.items() if k != "_id"}
        user["id"] = str(doc["_id"])

        return User(**user)

    def teardown_method(self) -> None:
        """Teardown any state that was previously setup."""
        for collection in self.database.list_collection_names():
            self.database.drop_collection(collection)

    def get_header(self, user: str, scopes: List[str]) -> dict:
        """get_header."""
        token = generate_jwt_token(user, scopes)

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        return request_headers
