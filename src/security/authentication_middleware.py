from functools import wraps
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException, Request
from jwt import decode
from jwt import exceptions as jwt_exceptions

from src.utils.exceptions_messages import ExceptionsMessages
from src.utils.settings import Settings

settings = Settings()


def authenticated(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=ExceptionsMessages.TOKEN_NOT_PROVIDED,
            )

        token = auth_header.split(' ')[1]

        try:
            payload = decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except jwt_exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=ExceptionsMessages.EXPIRED_TOKEN,
            )
        except jwt_exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=ExceptionsMessages.INVALID_TOKEN,
            )

        request.state.user_id = UUID(payload.get('sub'))

        return await func(request, *args, **kwargs)

    return wrapper
