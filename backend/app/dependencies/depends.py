from datetime import datetime
from typing import Callable, List, Tuple

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from pymongo.database import Database

from app.config.settings import get_settings
from app.dependencies.database import get_database
from app.repositories.base import BaseRepository
from app.repositories.cookie import CookieRepository
from app.repositories.password_staging import PasswordStagingRepository
from app.repositories.passwords import PasswordsRepository
from app.repositories.users import UserRepository
from app.services.authentication import AuthenticationService
from app.services.user import UserService


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
            password_repository: PasswordsRepository = Depends(
                get_repository(PasswordsRepository)
            ),
            password_staging_repository: PasswordStagingRepository = Depends(
                get_repository(PasswordStagingRepository)
            ),
        ) -> UserService:
            return UserService(
                user_repository=user_repository,
                password_repository=password_repository,
                password_staging_repository=password_staging_repository,
            )

        return _service

    if service_type == AuthenticationService:

        def _service(
            cookie_repository: CookieRepository = Depends(
                get_repository(CookieRepository)
            ),
            user_service: UserService = Depends(get_service(UserService)),
        ) -> AuthenticationService:
            return AuthenticationService(
                cookie_repository=cookie_repository,
                user_service=user_service,
            )

        return _service


def authenticated_user(
    roles: List[str] = [],
    return_token: bool = False,
) -> any:
    """Authenticate a user given a scope."""

    def _auth(
        request: Request,
        cookie_repository: CookieRepository = Depends(
            get_repository(CookieRepository)
        ),
    ) -> Tuple[str, str] | str:
        _settings = get_settings()

        token = None
        headers = request.get("headers")
        for header in headers:
            if header[0].decode().lower() == "authorization":
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

        _token = cookie_repository.get_by_id(email)
        if _token and _token.token != token:
            raise HTTPException(status_code=401, detail="Invalid Token")

        if return_token:
            return token
        return email

    return _auth
