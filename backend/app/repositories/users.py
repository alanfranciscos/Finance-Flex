from datetime import datetime
from typing import Dict

from bson import errors
from fastapi.exceptions import ValidationException
from pymongo.database import Database

from backend.app.repositories.base import BaseRepository
from backend.app.schemas.user import User
from backend.app.utils.datetime import set_default_timezone


class UserRepository(BaseRepository):
    """Class for UserRepository."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "users"
        self._user_collection = db[self._collection_name]

    def _create_user_from_mongo(self, user_dict: Dict) -> User:
        user = {
            k: set_default_timezone(v) if type(v) is datetime else v
            for k, v in user_dict.items()
        }

        user["id"] = user.pop("_id")

        return User(**user)

    def get_by_id(self, id: str) -> User:
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
            return self._create_user_from_mongo(doc)

        return None

    def create(self, user: User) -> User:
        """Insert a user."""
        src_user = user.model_dump()
        src_user["_id"] = src_user["id"]
        src_user.pop("id")

        self._user_collection.insert_one(src_user)
        return self.get_by_id(user.id)

    def update(self, user: User) -> User:
        """Update a user."""
        src_user = user.model_dump()
        src_user["_id"] = src_user["id"]
        src_user.pop("id")

        self._user_collection.update_one(
            {"_id": src_user["_id"]}, {"$set": src_user}
        )
        return self.get_by_id(user.id)
