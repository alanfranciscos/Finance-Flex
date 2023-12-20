from fastapi import APIRouter, Depends

from backend.app.dependencies.depends import get_service
from backend.app.schemas.authentication import Token
from backend.app.schemas.user import UserInput
from backend.app.services.authentication import AuthenticationService

router = APIRouter()


@router.get("/")
def authenticate_user(
    user_input: UserInput,
    auth_service: AuthenticationService = Depends(
        get_service(AuthenticationService)
    ),
) -> Token:
    """Authenticate user."""

    user = auth_service.authenticate(
        email=user_input.email, password=user_input.password
    )

    return user
