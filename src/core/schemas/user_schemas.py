from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.core.schemas.flashcard_schemas import FlashcardStackSchema

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
    flashcard_stacks: List[FlashcardStackSchema]

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: Optional[UserName] = None
    email: Optional[EmailStr] = None
