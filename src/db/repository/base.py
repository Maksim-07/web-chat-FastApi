from typing import Type

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BaseModel
from db.session import get_session


class BaseDatabaseRepository:
    _session: AsyncSession
    model: Type[BaseModel]

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    async def add(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self._session.execute(query)
        await self._session.commit()

    async def get_by(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
