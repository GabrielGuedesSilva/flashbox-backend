from src.core.services.base_service import BaseService
from src.database.models.flashcard_stack import FlashcardStack
from src.database.repositories.flashcard_stack_repository import (
    FlashcardStackRepository,
)


class FlashcardStackService(BaseService[FlashcardStack]):
    def __init__(self, flashcard_stack_repository: FlashcardStackRepository):
        super().__init__(flashcard_stack_repository, unique_fields=[])
