from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Request

from src.core.schemas.flashcard_schemas import (
    FlashcardStackCreateSchema,
    FlashcardStackSchema,
    FlashcardStackUpdateSchema,
)
from src.database.query import Query
from src.security.authentication_middleware import authenticated


class FlashcardStackRouter:
    def __init__(self, container):
        self.flashcard_stack_service = container.flashcard_stack_service()
        self.router = APIRouter(
            prefix='/flashcard_stacks',
            tags=['flashcard_stacks'],
        )

        @self.router.post(
            '',
            status_code=HTTPStatus.CREATED,
            response_model=FlashcardStackSchema,
        )
        @authenticated
        async def create_flashcard_stack(
            request: Request,
            flashcard_stack: FlashcardStackCreateSchema,
        ):
            flashcard_stack.user_id = request.state.user_id
            result = await self.flashcard_stack_service.add(flashcard_stack)
            return result

        @self.router.get(
            '',
            status_code=HTTPStatus.OK,
            response_model=List[FlashcardStackSchema],
        )
        @authenticated
        async def get_flashcard_stacks(
            request: Request,
        ):
            query = Query(request.query_params)
            query.filters['user_id'] = request.state.user_id
            flashcard_stacks = await self.flashcard_stack_service.get_all(query)
            return flashcard_stacks

        @self.router.get(
            '/{flashcard_stack_id}',
            status_code=HTTPStatus.OK,
            response_model=FlashcardStackSchema,
        )
        @authenticated
        async def get_flashcard_stack_by_id(
            request: Request,
            flashcard_stack_id: UUID,
        ):
            flashcard_stack = await self.flashcard_stack_service.get_by_id(
                flashcard_stack_id
            )
            return flashcard_stack

        @self.router.patch(
            '/{flashcard_stack_id}',
            status_code=HTTPStatus.OK,
            response_model=FlashcardStackSchema,
        )
        @authenticated
        async def update_flashcard_stack(
            request: Request,
            flashcard_stack_id: UUID,
            flashcard_stack: FlashcardStackUpdateSchema,
        ):
            updated_flashcard_stack = await self.flashcard_stack_service.update(
                flashcard_stack_id, flashcard_stack
            )
            return updated_flashcard_stack

        @self.router.delete(
            '/{flashcard_stack_id}', status_code=HTTPStatus.NO_CONTENT
        )
        @authenticated
        async def delete_flashcard_stack(
            request: Request,
            flashcard_stack_id: UUID,
        ):
            await self.flashcard_stack_service.remove(flashcard_stack_id)
