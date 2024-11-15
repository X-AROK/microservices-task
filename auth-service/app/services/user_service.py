from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)
