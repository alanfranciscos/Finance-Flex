from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.app.dependencies.depends import authenticated_user, get_service
from backend.app.schemas.users.authentication import Token
from backend.app.schemas.users.password import PasswordStagingValidate
from backend.app.schemas.users.user import User, UserAuthentication, UserInput
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


@router.post("/authenticate")
def authenticate_user(
    user_input: UserAuthentication,
    user_service: UserService = Depends(get_service(UserService)),
) -> Token:
    """Authenticate user.

    This endpoint receives a UserAuthentication, autheticate the User if
    credentials are valid and returns a Token.
    Body:
    - **UserAuthentication (UserAuthentication):**
        - email: str
        - password: str

    Return in body:
        - message: str

    Return in cookie:
    - **Token (Token):**
        - access_token: str
        - token_type: str: str
    """

    token = user_service.authenticate(
        email=user_input.email, password=user_input.password
    )
    response = JSONResponse(content={"message": "Authenticated"})
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=True,
    )
    return response


@router.get("/authenticate/renew")
def renew_token(
    user_service: UserService = Depends(get_service(UserService)),
    token: str = Depends(authenticated_user(return_token=True)),
) -> Token:
    """Renew token.

    This endpoint recive a Token in header request, renew it and
    returns a new Token.

    Return in body:
        - message: str

    Return in cookie:
    - **Token (Token):**
        - access_token: str
        - token_type: str: str
    """

    token = user_service.renew_token(token)
    response = JSONResponse(content={"message": "Authenticated"})
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=True,
    )

    return response


@router.post("/forgot-password")
def forgot_password(
    user_input: UserAuthentication,
    user_service: UserService = Depends(get_service(UserService)),
) -> PasswordStagingValidate:
    """Forot password.

    This endpoint recive a user id (email) and send a email with a
    code to reset the password.

    Body:
    - **UserAuthentication (UserAuthentication):**
        - email: str
        - password: str

    Return in cookie:
    - status: str
    """

    validate = user_service.request_forgot_password(
        id=user_input.email, password=user_input.password
    )

    return validate
