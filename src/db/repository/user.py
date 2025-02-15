from sqlalchemy import select

from db.models.user import User
from db.repository.base import BaseDatabaseRepository


class UserRepository(BaseDatabaseRepository[User]):
    model = User

    async def get_id_by_login(self, login: str) -> int | None:
        query = select(self.model.id).filter_by(login=login)
        result = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_login_by_id(self, user_id: int) -> str | None:
        query = select(self.model.login).filter_by(id=user_id)
        result = await self._session.execute(query)

        return result.scalar_one_or_none()
