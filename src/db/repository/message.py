from typing import Sequence

from sqlalchemy import select

from db.models.message import Message
from db.repository.base import BaseDatabaseRepository


class MessageRepository(BaseDatabaseRepository[Message]):
    model = Message

    async def get_messages_by_sender_id(self, sender_id: int) -> Sequence[str]:
        query = select(self.model.message).filter_by(sender_id=sender_id)
        result = await self._session.execute(query)
        return result.scalars().all()
