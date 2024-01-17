from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserVerification(BaseModel):
    verified: bool
    verification_code: str
    valid_until: datetime


class UserInput(BaseModel):
    email: str
    password: str
    name: str


class User(BaseModel):
    id: str
    email: str
    name: str
    roles: List[str] = []
    password: str
    verification: UserVerification
    created_at: datetime
    updated_at: datetime


class UserInformations(BaseModel):
    email: str
    name: str
    roles: List[str] = []
    verificated: bool


class UserValidationInput(BaseModel):
    email: str
    code: str
