from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
    from_user_id: int
    to_user_id: int
    status: str
    amount: Decimal
    created_at: datetime


class Transfer(BaseModel):
    to_user_id: int
    amount: Decimal


class Filter(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: Literal["SUCCESS", "FAILED"] | None = None
    page: int = 1
    on_page: int = 30
