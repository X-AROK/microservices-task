import bcrypt

from app.core.exceptions import AuthError
from app.core.jwt import create_token
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import ChangePassword, SignIn, SignUp
from app.services.base_service import BaseService


def get_hashed_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


class AuthService(BaseService):
    def __init__(self, repository: UserRepository) -> None:
        self.user_repository = repository
        super().__init__(repository)

    async def sign_in(self, data: SignIn):
        users = await self.user_repository.get_by_attr("login", data.login)
        if len(users) < 1:
            raise AuthError("Incorrect login or password")
        user = users[0]

        if not check_password(data.password, user.password):
            raise AuthError("Incorrect login or password")

        payload = {"user_id": user.id, "login": user.login}

        token = create_token(payload)

        return {"access_token": token, "user_id": user.id}

    async def sign_up(self, data: SignUp):
        data_copied = data.model_copy(
            update={"password": get_hashed_password(data.password)}
        )
        user = await self.user_repository.create(data_copied.model_dump(mode="python"))

        return user

    async def change_password(self, user_id: int, data: ChangePassword):
        user = await self.user_repository.get_by_id(user_id)

        if not check_password(data.old_password, user.password):
            raise AuthError("Incorrect password")

        user = await self.user_repository.update(
            user_id, {"password": get_hashed_password(data.new_password)}
        )

        return user
