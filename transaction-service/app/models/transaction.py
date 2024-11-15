from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Transaction(BaseModel):
    from_user_id: Mapped[int] = mapped_column()
    to_user_id: Mapped[int] = mapped_column()
    amount: Mapped[Decimal] = mapped_column()
    status: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())
