from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from src.database.models import Base


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    refresh_token = Column(String(555), nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
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
