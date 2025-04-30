from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth import UserManager
from .db import get_session
from models import AccessTokenModel, UserModel


async def get_access_token_db(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AsyncSession, None]:
    return AccessTokenModel.get_db(session)


def get_database_strategy(
    access_token_db: Annotated[
        AccessTokenDatabase[AccessTokenModel],
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    # Зависимость для получения стратегии выпуска токена.
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=86400,
    )


bearer_transport = BearerTransport(tokenUrl="/api/auth/login")
auth_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


async def get_users_db(
    session: Annotated[
        AsyncSession,
        Depends(get_session),
    ],
) -> AsyncGenerator[AsyncSession, None]:
    yield UserModel.get_db(session)


async def get_user_manager(
    user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_users_db)],
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


users = FastAPIUsers[UserModel, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)
current_user = users.current_user()
