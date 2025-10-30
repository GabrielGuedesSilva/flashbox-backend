from fastapi import APIRouter

from src.core.schemas.auth_schemas import (
    AuthTokenSchema,
    AuthUserResponseSchema,
    UserCredentialsSchema,
)


class AuthRouter:
    def __init__(self, container):
        self.auth_service = container.auth_service()
        self.router = APIRouter(
            prefix='/auth',
            tags=['Auth'],
        )

        @self.router.post('/', response_model=AuthTokenSchema)
        async def auth(
            credentials: UserCredentialsSchema,
        ):
            return await self.auth_service.auth(credentials)

        @self.router.post('/refresh', response_model=AuthUserResponseSchema)
        async def refresh_token(
            auth_token: AuthTokenSchema,
        ):
            return await self.auth_service.renew_token(auth_token)
