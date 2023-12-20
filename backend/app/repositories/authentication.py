from datetime import datetime
from typing import Dict

from bson import errors
from fastapi.exceptions import ValidationException
from pymongo.database import Database

from backend.app.repositories.base import BaseRepository
from backend.app.schemas.user import UserCredentials
from backend.app.utils.datetime import set_default_timezone


class AuthenticationRepository(BaseRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "users"
        self._user_collection = db[self._collection_name]

    def _create_user_credentials_from_mongo(
        self, user_dict: Dict
    ) -> UserCredentials:
        user = {
            k: set_default_timezone(v) if type(v) is datetime else v
            for k, v in user_dict.items()
            if k != "_id"
        }

        user["id"] = str(user_dict["_id"])

        return UserCredentials(**user)

    def get_credentials(self, id: str) -> UserCredentials:
        """Get a user by id.

        Parameters:
        id (string): user identifier.
        """
        try:
            doc = self._user_collection.find_one({"_id": id})
        except errors.InvalidId:
            raise ValidationException(
                "The Id entered is not a valid ObjectId."
            )

        if doc:
            return self._create_user_credentials_from_mongo(doc)

        return None
