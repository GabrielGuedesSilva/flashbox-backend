from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.models.auth_user import AuthUser
from src.database.repositories.base_repository import BaseRepository


class AuthUserRepository(BaseRepository[AuthUser]):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker, AuthUser)
