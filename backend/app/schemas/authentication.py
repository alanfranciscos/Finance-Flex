from pydantic import BaseModel


class AuthenticationInput(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
