from pydantic import BaseModel

from app.repository.base_repository import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    async def get_by_id(self, id: int):
        return await self.repository.get_by_id(id)

    async def add(self, entity: BaseModel):
        return await self.repository.create(entity.model_dump(mode="python"))

    async def update(self, params: BaseModel):
        return await self.repository.update(params.model_dump(mode="python"))

    async def delete(self, id: int):
        return await self.repository.delete(id)
