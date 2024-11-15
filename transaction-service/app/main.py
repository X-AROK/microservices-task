from fastapi import FastAPI

from app.core.config import config
from app.core.container import AppContainer
from app.routers.transaction_router import router as transaction_router

container = AppContainer()
app = FastAPI(title=config.APP_NAME)
app.include_router(transaction_router, prefix="/transactions")
