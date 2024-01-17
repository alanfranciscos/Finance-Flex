from datetime import datetime
from typing import List

from pydantic import BaseModel


class PasswordHeader(BaseModel):
    created_at: datetime
    password: str


class PasswordList(BaseModel):
    id: str
    passwords: List[PasswordHeader]


class PasswordStaging(BaseModel):
    id: str
    password: str
    code: str
    valid_until: datetime


class PasswordStagingValidate(BaseModel):
    id: str
    valid_until: datetime
