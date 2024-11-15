from fastapi import FastAPI

from app.core.config import config
from app.core.container import AppContainer
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

container = AppContainer()
app = FastAPI(title=config.APP_NAME)
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
