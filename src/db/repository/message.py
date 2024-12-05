from typing import Sequence

from sqlalchemy import Row, select

from db.models import User
from db.models.message import Message
from db.repository.base import BaseDatabaseRepository


class MessageRepository(BaseDatabaseRepository[Message]):
    model = Message

    async def get_messages_by_sender_id(self, sender_id: int) -> Sequence[str]:
        query = select(self.model.message).filter_by(sender_id=sender_id)
        result = await self._session.execute(query)

        return result.scalars().all()

    async def get_all_messages(self) -> Sequence[Row[tuple[str, str]]]:
        query = select(User.login, self.model.message).join(self.model, User.id == self.model.sender_id)
        result = await self._session.execute(query)

        return result.fetchmany()
