from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.models.flashcard_stack import FlashcardStack
from src.database.repositories.base_repository import BaseRepository


class FlashcardStackRepository(BaseRepository[FlashcardStack]):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker, FlashcardStack)
