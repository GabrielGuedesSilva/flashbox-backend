from src.core.schemas.user_schemas import UserCreateSchema
from src.core.services.base_service import BaseService
from src.database.models.user import User
from src.database.repositories.user_repository import UserRepository
from src.security.hash_functions import get_password_hash


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, unique_fields=['email'])

    async def add(self, schema: UserCreateSchema) -> User:
        schema.password = get_password_hash(schema.password)
        return await super().add(schema)
