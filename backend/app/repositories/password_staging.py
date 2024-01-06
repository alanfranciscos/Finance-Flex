from datetime import datetime
from typing import Dict

from bson import errors
from pymongo.database import Database

from backend.app.repositories.base import BaseRepository
from backend.app.schemas.passwords import (
    PasswordStaging,
    PasswordStagingValidate,
)
from backend.app.utils import api_errors
from backend.app.utils.datetime import set_default_timezone


class PsswordStagingRepository(BaseRepository):
    """Class for PsswordStagingRepository."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "users.passwords-staging"
        self._passwords_repository = db[self._collection_name]

    def _create_password_from_mongo(
        self, password_dict: Dict
    ) -> PasswordStaging:
        password = {
            k: set_default_timezone(v) if type(v) is datetime else v
            for k, v in password_dict.items()
        }

        return PasswordStaging(
            id=password["_id"],
            password=password["password"],
            code=password["code"],
            valid_until=password["valid_until"],
        )

    def get_by_id(self, id) -> PasswordStaging:
        """Get a list of passwords.

        Parameters:
        id (string): user identifier.
        """
        try:
            doc = self._passwords_repository.find_one({"_id": id})
        except errors.InvalidId:
            return None

        if doc:
            return self._create_password_from_mongo(doc)

    def save_password_staging(
        self, password_staging: PasswordStaging
    ) -> PasswordStagingValidate:
        """save password in staging area.

        Parameters:
        **password_staging (PasswordStaging)**:
           - id: str
           - password: str
           - code: str
           - valid_until: datetime

        """
        src_password = password_staging.model_dump()
        src_password["_id"] = src_password["id"]
        src_password.pop("id")

        try:
            doc = self.get_by_id(password_staging.id)
        except errors.InvalidId:
            api_errors.raise_error_response(
                api_errors.ErrorResourceDataInvalid,
                detail="Invalid id",
            )

        if not doc:
            self._passwords_repository.insert_one(src_password)
        elif doc.valid_until.replace(tzinfo=None) > datetime.utcnow():
            api_errors.raise_error_response(
                api_errors.ErrorResourceDataInvalid,
                detail="Password already requested",
            )
        else:
            self._passwords_repository.replace_one(
                filter={"_id": password_staging.id}, replacement=src_password
            )

        password_staging_created = self.get_by_id(password_staging.id)

        password_staging_validate = PasswordStagingValidate(
            id=password_staging_created.id,
            valid_until=password_staging_created.valid_until,
        )

        return password_staging_validate
