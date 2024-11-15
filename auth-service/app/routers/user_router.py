from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import AppContainer
from app.schema.user_schema import UserBase
from app.services.user_service import UserService

router = APIRouter(tags=["user"])


@router.get("/{id}", response_model=UserBase)
@inject
async def user_by_id(
    id: int, user_service: UserService = Depends(Provide[AppContainer.user_service])
):
    return await user_service.get_by_id(id)
