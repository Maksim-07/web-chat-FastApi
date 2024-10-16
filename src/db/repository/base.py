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
        new_instance = insert(self.model).values(**kwargs)
        await self._session.execute(new_instance)
        await self._session.commit()

    async def get_by(self, **filter_by) -> BaseModel | None:
        new_instance = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(new_instance)
        return result.scalar_one_or_none()
