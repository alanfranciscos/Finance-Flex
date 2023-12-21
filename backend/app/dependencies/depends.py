from datetime import datetime
from typing import Callable, List, Tuple

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from pymongo.database import Database

from backend.app.config.settings import get_settings
from backend.app.dependencies.database import get_database
from backend.app.repositories.base import BaseRepository
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import User
from backend.app.services.user import UserService


def authenticated_user(
    roles: List[str] = [], return_token: bool = False
) -> any:
    """Authenticate a user given a scope."""

    def _auth(request: Request) -> Tuple[User]:
        _settings = get_settings()

        token = None
        headers = request.get("headers")
        for header in headers:
            if header[0].decode() == "authorization":
                token = header[1].decode().split(" ")[1]
                break

        try:
            payload = jwt.decode(
                token,
                _settings.JWT_SECRET_KEY,
                algorithms=[_settings.JWT_ALGORITHM],
            )
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Token {e}")

        email = payload.get("user")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid Email")

        if roles:
            for role in roles:
                if role not in payload.get("roles"):
                    raise HTTPException(
                        status_code=401,
                        detail=f"Invalid role {role}",
                    )

        payload_time = datetime.utcfromtimestamp(payload.get("exp"))
        if payload_time < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")

        if return_token:
            return token
        return email

    return _auth


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[Database], BaseRepository]:
    """Get a repository as callable."""
    if repo_type == UserRepository:

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
            return UserService(user_repository=user_repository)

        return _service
