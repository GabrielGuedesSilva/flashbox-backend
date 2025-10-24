from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.models.flashcard import Flashcard
from src.database.repositories.base_repository import BaseRepository


class FlashcardRepository(BaseRepository[Flashcard]):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker, Flashcard)
