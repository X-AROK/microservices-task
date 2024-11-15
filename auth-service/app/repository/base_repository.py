from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, EntityError, NotFoundError
from app.models.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        sessionmaker: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        model: type[T],
    ) -> None:
        self.sessionmaker = sessionmaker
        self.model = model

    async def get_by_id(self, id: int):
        async with self.sessionmaker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            entity = result.scalar_one_or_none()
            if not entity:
                raise NotFoundError(detail=f"id {id} not found")
            return entity

    async def get_by_attr(self, column: str, value: Any):
        attr = getattr(self.model, column, None)
        if attr is None:
            raise EntityError(f"attr {attr} not found")

        async with self.sessionmaker() as session:
            stmt = select(self.model).where(attr == value)
            result = await session.execute(stmt)
            entities = result.scalars().all()
            return entities

    async def create(self, data: dict):
        async with self.sessionmaker() as session:
            entity = self.model(**data)
            try:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
            except IntegrityError:
                raise AlreadyExistsError("Duplicate")
            return entity

    async def update(self, id: int, data: dict):
        async with self.sessionmaker() as session:
            stmt = update(self.model).where(self.model.id == id).values(data)
            await session.execute(stmt)
            await session.commit()

        return await self.get_by_id(id)

    async def delete(self, id: int):
        entity = await self.get_by_id(id)

        async with self.sessionmaker() as session:
            await session.delete(entity)
            await session.commit()
