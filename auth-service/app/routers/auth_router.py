from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import AppContainer
from app.core.dependencies import get_current_user_id
from app.core.logger import log
from app.schema.auth_schema import ChangePassword, SignIn, SignUp, Token
from app.schema.user_schema import UserBase
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/sign-up", response_model=UserBase)
@inject
@log(
    on_success="Регистрация пользователя {login} прошла успешно.",
    on_failure="При регистрации произошла ошибка: '{error}'",
)
async def sign_up(
    data: SignUp,
    auth_service: AuthService = Depends(Provide[AppContainer.auth_service]),
):
    return await auth_service.sign_up(data)


@router.post("/sign-in", response_model=Token)
@inject
@log(
    on_success="Пользователь с ID {user_id} вошел в систему.",
    on_failure="При попытке входа произошла ошибка: '{error}'",
)
async def sign_in(
    data: SignIn,
    auth_service: AuthService = Depends(Provide[AppContainer.auth_service]),
):
    return await auth_service.sign_in(data)


@router.post("/change-password", response_model=UserBase)
@inject
@log(
    on_success="Пользователь {login} сменил пароль.",
    on_failure="При попытке смены пароля произошла ошибка: '{error}'",
)
async def change_password(
    data: ChangePassword,
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: AuthService = Depends(Provide[AppContainer.auth_service]),
):
    return await auth_service.change_password(user_id, data)
