from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from .types import UserName


class UserCreateSchema(BaseModel):
    username: UserName
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: UUID
    username: UserName
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: Optional[UserName] = None
    email: Optional[EmailStr] = None
