from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.models import Base


class FlashcardStack(Base):
    __tablename__ = 'flashcard_stacks'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    title = Column(String(50), nullable=False)
    main_language = Column(String(65), nullable=False)
    learning_language = Column(String(65), nullable=False)
    flashcards = relationship(
        'Flashcard',
        back_populates='flashcard_stack',
        lazy='selectin',
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
    )
    user = relationship(
        'User', back_populates='flashcard_stacks', passive_deletes=True
    )
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
