from typing import List

from pydantic import BaseModel


class UserVerification(BaseModel):
    verified: bool
    verification_code: str


class Create_user(BaseModel):
    id: str
    email: str
    name: str
    roles: List[str] = []
    password: str
    verification: UserVerification
    created_at: str
    updated_at: str


class UserCredentials(BaseModel):
    email: str
    name: str
    password: str
    roles: List[str] = []
    verification: UserVerification


class UserInput(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    name: str
    roles: List[str] = []
    verificated: bool
