from pymongo.database import Database


class BaseRepository:
    """Class that defines BaseRepository."""

    def __init__(self, db: Database) -> None:
        self.db = db
        self._protected_properties = ["id"]
