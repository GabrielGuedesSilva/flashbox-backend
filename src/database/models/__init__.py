from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Base', 'User', 'Flashcard', 'FlashcardStack', 'AuthUser']

Base = declarative_base()

from src.database.models.auth_user import AuthUser
from src.database.models.flashcard import Flashcard
from src.database.models.flashcard_stack import FlashcardStack
from src.database.models.user import User
