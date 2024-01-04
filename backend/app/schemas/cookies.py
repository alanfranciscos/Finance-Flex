from pydantic import BaseModel


class Cookie(BaseModel):
    id: str
    token: str


class CookieResponse(BaseModel):
    token: str
