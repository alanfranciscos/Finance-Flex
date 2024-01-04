from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.app.dependencies.depends import authenticated_user, get_service
from backend.app.schemas.authentication import AuthenticationInput, Token
from backend.app.services.authentication import AuthenticationService

router = APIRouter()


@router.post("")
def authenticate_user(
    user_input: AuthenticationInput,
    auth_service: AuthenticationService = Depends(
        get_service(AuthenticationService)
    ),
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

    token = auth_service.authenticate(
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


@router.get("/renew")
def renew_token(
    auth_service: AuthenticationService = Depends(
        get_service(AuthenticationService)
    ),
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

    token = auth_service.renew_token(token)
    response = JSONResponse(content={"message": "Authenticated"})
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=True,
    )

    return response
