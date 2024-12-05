from fastapi import Depends

from db.repository.user import UserRepository
from schemas.users import UserIdSchema, UserLoginSchema


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_user_id(self, login: str) -> UserIdSchema:
        user_id = await self.user_repo.get_id_by_login(login=login)

        return UserIdSchema(id=user_id)

    async def get_user_login(self, id_user: int) -> UserLoginSchema:
        login = await self.user_repo.get_login_by_id(user_id=id_user)

        return UserLoginSchema(login=login)
