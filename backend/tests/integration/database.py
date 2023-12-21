from pymongo import MongoClient
from pymongo.database import Database

from backend.tests.integration.settings import get_settings

_mongo = None


def get_mongo() -> MongoClient:
    """Get MongoClient instance."""
    global _mongo
    if not _mongo:
        _mongo = MongoClient(
            get_settings().MONGO_URI,
            connect=False,
            maxPoolSize=2,
            maxConnecting=2,
            maxIdleTimeMS=5000,
            timeoutMS=60000,
            waitQueueTimeoutMS=30000,
        )
    return _mongo


def get_database() -> Database:
    """Get current database client instance."""
    return get_mongo()[get_settings().MONGO_DATABASE]


def close_connection() -> None:
    """Close current database client connection."""
    get_mongo().close()
