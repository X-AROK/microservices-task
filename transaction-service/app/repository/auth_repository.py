from aiohttp import ClientSession


class AuthRepository:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def is_user_register(self, user_id: int) -> bool:
        async with ClientSession(self.base_url) as session:
            async with session.get(f"/users/{user_id}") as response:
                return response.status == 200
