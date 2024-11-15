from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class User(BaseModel):
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
