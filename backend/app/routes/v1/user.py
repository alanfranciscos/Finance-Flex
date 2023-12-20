from fastapi import APIRouter, Depends

from backend.app.dependencies.depends import get_service
from backend.app.schemas.user import User, UserInput
from backend.app.services.user import UserService

router = APIRouter()


@router.post("", status_code=201)
def create_user(
    user_input: UserInput,
    user_service: UserService = Depends(get_service(UserService)),
) -> User:
    """Create user.

    This endpoint receives a UserInput, create a User document in
      database and returns it.
    Body:
    - **UserInput (UserInput):**
        - email: str
        - password: str

    Returns:
    - **User (User):**
        - email: str
        - scopes: List[str] = []
    """

    user = user_service.create(
        user_input=user_input,
    )

    return user
