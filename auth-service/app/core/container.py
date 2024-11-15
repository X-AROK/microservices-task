from dependency_injector import containers, providers

from app.core.config import config
from app.core.database import Database
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.routers.auth_router", "app.routers.user_router"]
    )

    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

    user_repository = providers.Factory(
        UserRepository, sessionmaker=db.provided.session
    )

    auth_service = providers.Factory(AuthService, repository=user_repository)
    user_service = providers.Factory(UserService, repository=user_repository)
