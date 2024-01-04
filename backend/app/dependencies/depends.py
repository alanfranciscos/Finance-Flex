from typing import Callable

from fastapi import Depends
from pymongo.database import Database

from backend.app.dependencies.database import get_database
from backend.app.repositories.base import BaseRepository
from backend.app.repositories.users import UserRepository
from backend.app.services.user import UserService


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[Database], BaseRepository]:
    """Get a repository as callable."""

    def _get_repo(db: Database = Depends(get_database)) -> BaseRepository:
        return repo_type(db)

    return _get_repo


def get_service(service_type: type[any]) -> Callable:
    """Get a service as callable."""
    if service_type == UserService:

        def _service(
            user_repository: UserRepository = Depends(
                get_repository(UserRepository)
            ),
        ) -> UserService:
            return UserService(
                user_repository=user_repository,
            )

        return _service
