from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class Message(BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(String, nullable=False)
