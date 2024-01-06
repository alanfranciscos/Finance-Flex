from fastapi import APIRouter, Depends

from backend.app.dependencies.depends import get_service
from backend.app.schemas.authentication import AuthenticationInput
from backend.app.schemas.passwords import PasswordStagingValidate
from backend.app.schemas.user import UserInformations, UserInput
from backend.app.services.user import UserService

router = APIRouter()


@router.post("", status_code=201)
def create_user(
    user_input: UserInput,
    user_service: UserService = Depends(get_service(UserService)),
) -> UserInformations:
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


@router.post("/forgot-password")
def forgot_password(
    user_input: AuthenticationInput,
    user_service: UserService = Depends(get_service(UserService)),
) -> PasswordStagingValidate:
    """Forot password.

    This endpoint recive a user id (email) and send a email with a
    code to reset the password.

    Body:
    - **UserAuthentication (UserAuthentication):**
        - email: str
        - code: str

    Return in cookie:
    - status: str
    """

    validate = user_service.request_forgot_password(
        id=user_input.email, password=user_input.password
    )

    return validate
