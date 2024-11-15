from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(
        self,
        sessionmaker: Callable[
            ..., AbstractAsyncContextManager[AsyncSession, bool | None]
        ],
    ) -> None:
        super().__init__(sessionmaker, User)
