from datetime import timezone
from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.integration.create_db_doc import CreateDbDoc
from tests.integration.database import (
    get_database as get_database_tests,
)
from tests.integration.helper import (
    generate_jwt_token,
    set_envs_for_tests,
)
from tests.integration.settings import (
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
            from app.config.settings import get_settings
            from app.dependencies.database import get_database
            from app.main import app

            app.dependency_overrides[get_settings] = get_settings_tests
            app.dependency_overrides[get_database] = get_database_tests

            return app

        cls.app_client = TestClient(_get_app())

        cls.database = get_database_tests()

        def _create_database_doc() -> CreateDbDoc:
            """create_database_doc."""
            return CreateDbDoc(
                database=cls.database,
            )

        cls.create_database_doc: CreateDbDoc = _create_database_doc()

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
