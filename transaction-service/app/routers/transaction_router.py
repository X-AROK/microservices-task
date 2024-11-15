from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.core.container import AppContainer
from app.core.dependencies import get_current_user_id
from app.core.logger import log
from app.schema.transaction_schema import Filter, Transaction, Transfer
from app.services.transaction_service import TransactionService

router = APIRouter(tags=["transaction"])


@router.post("/transfer", response_model=Transaction)
@inject
@log(
    on_success="Пользователем {from_user_id} произвел транзацию. Пользователю: {to_user_id}, количество: {amount}, статус: {status}",
    on_failure="При произведении транзакции произршла ошибка: '{error}'",
)
async def transfer(
    data: Transfer,
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    transaction_service: TransactionService = Depends(
        Provide[AppContainer.transaction_service]
    ),
):
    return await transaction_service.transfer(current_user_id, data)


@router.get("/", response_model=list[Transaction])
@inject
async def all(
    filters: Annotated[Filter, Query()],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    transaction_service: TransactionService = Depends(
        Provide[AppContainer.transaction_service]
    ),
):
    return await transaction_service.get_list(current_user_id, filters)
