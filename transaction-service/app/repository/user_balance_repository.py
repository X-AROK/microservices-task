from contextlib import AbstractAsyncContextManager
from decimal import Decimal
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_balance import UserBalance
from app.repository.base_repository import BaseRepository


class UserBalanceRepository(BaseRepository[UserBalance]):
    def __init__(
        self,
        sessionmaker: Callable[
            ..., AbstractAsyncContextManager[AsyncSession, bool | None]
        ],
    ) -> None:
        super().__init__(sessionmaker, UserBalance)

    async def transfer(self, from_id: int, to_id: int, amount: Decimal):
        async with self.sessionmaker() as session:
            stmt = (
                select(self.model)
                .where(self.model.user_id == from_id)
                .with_for_update()
            )
            res = await session.execute(stmt)
            from_balance = res.scalar_one_or_none()
            if from_balance is None:
                from_balance = await self.create({"user_id": from_id})

            if from_balance.balance < amount:
                return False

            stmt = (
                select(self.model).where(self.model.user_id == to_id).with_for_update()
            )
            res = await session.execute(stmt)
            to_balance = res.scalar_one_or_none()
            if to_balance is None:
                to_balance = await self.create({"user_id": to_id})

            from_balance.balance -= amount
            to_balance.balance += amount
            session.add(from_balance)
            session.add(to_balance)
            await session.commit()

            return True
