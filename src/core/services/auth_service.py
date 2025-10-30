from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import HTTPException

from src.core.schemas.auth_schemas import (
    AuthTokenSchema,
    AuthUserCreateSchema,
    AuthUserResponseSchema,
    AuthUserUpdateSchema,
    UserCredentialsSchema,
)
from src.database.query import Query
from src.database.repositories.auth_user_repository import AuthUserRepository
from src.security.auth_functions import (
    create_access_token,
    create_refresh_token,
    update_exp_access_token,
    verify_refresh_token,
)
from src.security.hash_functions import verify_password
from src.utils.settings import Settings

from .user_service import UserService

settings = Settings()


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        auth_user_repository: AuthUserRepository,
    ):
        self.user_service = user_service
        self.auth_user_repository = auth_user_repository

    async def auth(self, credentials):
        user = None

        if isinstance(credentials, UserCredentialsSchema):
            query = Query({
                'email': credentials.email,
            })
            user = await self.user_service.get_one(query)

        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found',
            )

        is_valid_credentials = False

        if user:
            is_valid_credentials = verify_password(
                credentials.password, user.password
            )

        if not is_valid_credentials:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Incorrect email or password',
            )

        user_id = user.id

        now = datetime.now(timezone.utc)
        access_token = create_access_token(
            payload={
                'sub': str(user_id),
                'iat': now,
                'exp': now
                + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
            }
        )

        refresh_token = create_refresh_token(access_token)

        query_registered_auth_user = Query({'user_id': user_id})
        registered_auth_user = await self.auth_user_repository.find_one(
            query_registered_auth_user
        )

        if not registered_auth_user:
            auth_user = AuthUserCreateSchema(
                refresh_token=refresh_token, user_id=user_id
            )
            await self.auth_user_repository.create(auth_user)
        else:
            update_auth_user = AuthUserUpdateSchema(refresh_token=refresh_token)
            await self.auth_user_repository.update(
                registered_auth_user.id, update_auth_user
            )

        result = AuthTokenSchema(
            access_token=access_token, refresh_token=refresh_token
        )

        return result

    async def renew_token(self, auth_token: AuthTokenSchema):
        if not isinstance(auth_token, AuthTokenSchema):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Invalid token schema',
            )

        access_token = auth_token.access_token
        refresh_token = auth_token.refresh_token

        query_registered_auth_user = Query({'refresh_token': refresh_token})

        registered_auth_user = await self.auth_user_repository.find_one(
            query_registered_auth_user
        )

        refresh_token_is_valid = verify_refresh_token(
            access_token, refresh_token
        )

        if not registered_auth_user or not refresh_token_is_valid:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid token or refresh token',
            )

        renewed_access_token = update_exp_access_token(access_token)
        new_refresh_token = create_refresh_token(renewed_access_token)

        update_auth_user = AuthUserUpdateSchema(refresh_token=new_refresh_token)
        await self.auth_user_repository.update(
            registered_auth_user.id, update_auth_user
        )

        result = AuthUserResponseSchema(
            user_id=registered_auth_user.user_id,
            access_token=renewed_access_token,
            refresh_token=new_refresh_token,
        )

        return result
