from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserVerification(BaseModel):
    verified: bool
    verification_code: str
    valid_until: datetime


class Create_user(BaseModel):
    id: str
    email: str
    name: str
    roles: List[str] = []
    password: str
    verification: UserVerification
    created_at: datetime
    updated_at: datetime


class UserCredentials(BaseModel):
    email: str
    name: str
    password: str
    roles: List[str] = []
    verification: UserVerification


class UserInput(BaseModel):
    email: str
    password: str
    name: str


class User(BaseModel):
    email: str
    name: str
    roles: List[str] = []
    verificated: bool


class UserAuthentication(BaseModel):
    email: str
    password: str


class UserVerification(BaseModel):
    code: str
    valid_until: datetime
