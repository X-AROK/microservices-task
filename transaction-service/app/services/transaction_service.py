from app.core.exceptions import EntityError, NotFoundError
from app.repository.auth_repository import AuthRepository
from app.repository.transaction_repository import TransactionRepository
from app.repository.user_balance_repository import UserBalanceRepository
from app.schema.transaction_schema import Filter, Transfer
from app.services.base_service import BaseService


class TransactionService(BaseService):
    def __init__(
        self,
        user_balance_repository: UserBalanceRepository,
        transaction_repository: TransactionRepository,
        auth_repository: AuthRepository,
    ) -> None:
        self.user_balance_repository = user_balance_repository
        self.transaction_repository = transaction_repository
        self.auth_repository = auth_repository
        super().__init__(user_balance_repository)

    async def transfer(self, current_user_id: int, data: Transfer):
        if current_user_id == data.to_user_id:
            raise EntityError("you can not send money to yourself")

        is_registered = await self.auth_repository.is_user_register(data.to_user_id)
        if not is_registered:
            raise NotFoundError("user not found")

        is_success = await self.user_balance_repository.transfer(
            current_user_id, data.to_user_id, data.amount
        )

        transaction = await self.transaction_repository.create(
            {
                "from_user_id": current_user_id,
                "to_user_id": data.to_user_id,
                "amount": data.amount,
                "status": "SUCCESS" if is_success else "FAILED",
            }
        )

        return transaction

    async def get_list(self, current_user_id: int, filters: Filter):
        transactions = await self.transaction_repository.get_list(
            current_user_id,
            filters.start_date,
            filters.end_date,
            filters.status,
            filters.on_page,
            filters.page,
        )

        return transactions
