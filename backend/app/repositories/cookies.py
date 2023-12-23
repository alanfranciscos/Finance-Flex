from datetime import datetime
from typing import Dict

from bson import errors
from fastapi.exceptions import ValidationException
from pymongo.database import Database

from backend.app.repositories.base import BaseRepository
from backend.app.schemas.cookies import Cookie, CookieResponse
from backend.app.utils.datetime import set_default_timezone


class CookieRepository(BaseRepository):
    """Class for CookieRepository."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "cookies"
        self._cookie_repository = db[self._collection_name]

    def _create_cookie_from_mongo(self, cookie_dict: Dict) -> CookieResponse:
        cookie = {
            k: set_default_timezone(v) if type(v) is datetime else v
            for k, v in cookie_dict.items()
            if k != "_id"
        }

        return CookieResponse(
            token=cookie["token"],
        )

    def get_by_id(self, id: str) -> CookieResponse:
        """Get a cookie by id of user.

        Parameters:
        id (string): user identifier.
        """
        try:
            doc = self._cookie_repository.find_one({"_id": id})
        except errors.InvalidId:
            raise ValidationException(
                "The Id entered is not a valid ObjectId."
            )

        if doc:
            return self._create_cookie_from_mongo(doc)

        return None

    def Save(self, cookie: Cookie) -> CookieResponse:
        """Save user cookie."""
        src_cookie = cookie.model_dump()
        src_cookie["_id"] = src_cookie["id"]
        src_cookie.pop("id")

        doc = self.get_by_id(cookie.id)
        if not doc:
            self._cookie_repository.insert_one(src_cookie)
        else:
            self._cookie_repository.replace_one(
                filter={"_id": cookie.id}, replacement=src_cookie
            )
        return self.get_by_id(cookie.id)
