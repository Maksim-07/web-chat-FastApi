from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
