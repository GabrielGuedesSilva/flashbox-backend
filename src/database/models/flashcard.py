from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.models import Base


class Flashcard(Base):
    __tablename__ = 'flashcards'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    word_to_learn = Column(String(50), nullable=False)
    translation = Column(String(50), nullable=False)
    example = Column(String(100), nullable=True)
    flashcard_stack_id = Column(
        UUID(as_uuid=True),
        ForeignKey('flashcard_stacks.id', ondelete='SET NULL'),
        nullable=True,
    )
    flashcard_stack = relationship('FlashcardStack', passive_deletes=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
