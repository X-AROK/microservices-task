from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class UserBalance(BaseModel):
    user_id: Mapped[int] = mapped_column(unique=True)
    balance: Mapped[Decimal] = mapped_column(default=0)
