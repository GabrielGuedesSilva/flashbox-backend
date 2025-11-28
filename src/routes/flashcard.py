from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Request

from src.core.schemas.flashcard_schemas import (
    FlashcardCreateSchema,
    FlashcardSchema,
    FlashcardUpdateSchema,
)
from src.database.query import Query
from src.security.authentication_middleware import authenticated


class FlashcardRouter:
    def __init__(self, container):
        self.flashcard_service = container.flashcard_service()
        self.router = APIRouter(
            prefix='/flashcards',
            tags=['flashcards'],
        )

        @self.router.post(
            '', status_code=HTTPStatus.CREATED, response_model=FlashcardSchema
        )
        @authenticated
        async def create_flashcard(
            request: Request,
            flashcard: FlashcardCreateSchema,
        ):
            flashcard.user_id = request.state.user_id
            result = await self.flashcard_service.add(flashcard)
            return result

        @self.router.get(
            '', status_code=HTTPStatus.OK, response_model=List[FlashcardSchema]
        )
        @authenticated
        async def get_flashcards(
            request: Request,
        ):
            query = Query(request.query_params)
            query.filters['user_id'] = request.state.user_id
            flashcards = await self.flashcard_service.get_all(query)
            return flashcards

        @self.router.get(
            '/{flashcard_id}',
            status_code=HTTPStatus.OK,
            response_model=FlashcardSchema,
        )
        @authenticated
        async def get_flashcard_by_id(
            request: Request,
            flashcard_id: UUID,
        ):
            flashcard = await self.flashcard_service.get_by_id(flashcard_id)
            return flashcard

        @self.router.patch(
            '/{flashcard_id}',
            status_code=HTTPStatus.OK,
            response_model=FlashcardSchema,
        )
        @authenticated
        async def update_flashcard(
            request: Request,
            flashcard_id: UUID,
            flashcard: FlashcardUpdateSchema,
        ):
            updated_flashcard = await self.flashcard_service.update(
                flashcard_id, flashcard
            )
            return updated_flashcard

        @self.router.delete(
            '/{flashcard_id}', status_code=HTTPStatus.NO_CONTENT
        )
        @authenticated
        async def delete_flashcard(
            request: Request,
            flashcard_id: UUID,
        ):
            await self.flashcard_service.remove(flashcard_id)
