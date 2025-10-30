from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .types import NonEmptyStr


class FlashcardCreateSchema(BaseModel):
    word_to_learn: NonEmptyStr
    translation: NonEmptyStr
    example: Optional[NonEmptyStr] = None
    flashcard_stack_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class FlashcardSchema(BaseModel):
    id: UUID
    word_to_learn: NonEmptyStr
    translation: NonEmptyStr
    example: Optional[NonEmptyStr] = None
    flashcard_stack_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FlashcardUpdateSchema(BaseModel):
    word_to_learn: Optional[NonEmptyStr] = None
    translation: Optional[NonEmptyStr] = None
    example: Optional[NonEmptyStr] = None
    flashcard_stack_id: Optional[UUID] = None


class FlashcardStackCreateSchema(BaseModel):
    title: NonEmptyStr
    main_language: NonEmptyStr
    learning_language: NonEmptyStr
    user_id: Optional[UUID] = None


class FlashcardStackSchema(BaseModel):
    id: UUID
    title: NonEmptyStr
    main_language: NonEmptyStr
    learning_language: NonEmptyStr
    flashcards: Optional[List[FlashcardSchema]] = None
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FlashcardStackUpdateSchema(BaseModel):
    title: Optional[NonEmptyStr] = None
    main_language: Optional[NonEmptyStr] = None
    learning_language: Optional[NonEmptyStr] = None
