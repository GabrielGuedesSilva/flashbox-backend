from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.services.auth_service import AuthService
from src.core.services.flashcard_service import FlashcardService
from src.core.services.flashcard_stack_service import FlashcardStackService
from src.core.services.user_service import UserService
from src.database.repositories import (
    AuthUserRepository,
    FlashcardRepository,
    FlashcardStackRepository,
    UserRepository,
)


class Container(containers.DeclarativeContainer):
    # Config
    config = providers.Configuration()

    # Engine
    engine = providers.Singleton(
        create_async_engine,
        config.DATABASE_URL,
    )

    # Async sessionmaker
    async_sessionmaker = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    # Repositories
    user_repository = providers.Factory(
        UserRepository, sessionmaker=async_sessionmaker
    )
    flashcard_repository = providers.Factory(
        FlashcardRepository, sessionmaker=async_sessionmaker
    )
    flashcard_stack_repository = providers.Factory(
        FlashcardStackRepository, sessionmaker=async_sessionmaker
    )
    auth_user_repository = providers.Factory(
        AuthUserRepository, sessionmaker=async_sessionmaker
    )

    # Services
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )
    flashcard_service = providers.Factory(
        FlashcardService, flashcard_repository=flashcard_repository
    )
    flashcard_stack_service = providers.Factory(
        FlashcardStackService,
        flashcard_stack_repository=flashcard_stack_repository,
    )
    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        auth_user_repository=auth_user_repository,
    )
