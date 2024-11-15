from contextlib import AbstractAsyncContextManager
from datetime import datetime
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repository.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(
        self,
        sessionmaker: Callable[
            ..., AbstractAsyncContextManager[AsyncSession, bool | None]
        ],
    ) -> None:
        super().__init__(sessionmaker, Transaction)

    async def get_list(
        self,
        user_id: int,
        start_date: datetime | None,
        end_date: datetime | None,
        status: str | None,
        limit: int,
        page: int,
    ):
        async with self.sessionmaker() as session:
            stmt = select(self.model).where(self.model.from_user_id == user_id)
            if start_date is not None:
                stmt = stmt.where(self.model.created_at >= start_date)
            if end_date is not None:
                stmt = stmt.where(self.model.created_at <= end_date)
            if status is not None:
                stmt = stmt.where(self.model.status == status)

            stmt = stmt.limit(limit).offset(limit * (page - 1))

            result = await session.execute(stmt)
            entities = result.scalars().all()

            return entities
