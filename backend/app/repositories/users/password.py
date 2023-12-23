from datetime import datetime
from typing import Dict

from bson import errors
from pymongo.database import Database

from backend.app.repositories.base import BaseRepository
from backend.app.schemas.users.password import PasswordList
from backend.app.utils.datetime import set_default_timezone


class PasswordsRepository(BaseRepository):
    """Class for PasswordsRepository."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "users.password"
        self._passwords_repository = db[self._collection_name]

    def _create_password_from_mongo(self, password_dict: Dict) -> PasswordList:
        password = {
            k: set_default_timezone(v) if type(v) is datetime else v
            for k, v in password_dict.items()
            if k != "_id"
        }
        password["id"] = password["_id"]

        return PasswordList(
            passwords=password["passwords"],
        )

    def get_passwords_from_user(self, id) -> PasswordList:
        """Get a list of passwords.

        Parameters:
        id (string): user identifier.
        """
        try:
            doc = self._passwords_repository.find_one({"_id": id})

        except errors.InvalidId:
            return None

        if doc:
            return self._create_password_from_mongo(id)
