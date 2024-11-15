from dependency_injector import containers, providers

from app.core.config import config
from app.core.database import Database
from app.repository.auth_repository import AuthRepository
from app.repository.transaction_repository import TransactionRepository
from app.repository.user_balance_repository import UserBalanceRepository
from app.services.transaction_service import TransactionService


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.routers.transaction_router"]
    )

    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

    user_balance_repository = providers.Factory(
        UserBalanceRepository, sessionmaker=db.provided.session
    )
    transaction_repository = providers.Factory(
        TransactionRepository, sessionmaker=db.provided.session
    )
    auth_repository = providers.Factory(
        AuthRepository, base_url=config.AUTH_SERVICE_URL
    )

    transaction_service = providers.Factory(
        TransactionService,
        user_balance_repository=user_balance_repository,
        transaction_repository=transaction_repository,
        auth_repository=auth_repository,
    )
