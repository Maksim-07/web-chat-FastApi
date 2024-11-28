from typing import Generic, Type, TypeVar, Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session

T = TypeVar("T")


class BaseDatabaseRepository(Generic[T]):
    _session: AsyncSession
    model: Type[T]

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    async def add(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self._session.execute(query)
        await self._session.commit()

    async def get_by(self, **filter_by) -> T | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[T]:
        query = select(self.model)
        result = await self._session.execute(query)
        return result.scalars().all()
