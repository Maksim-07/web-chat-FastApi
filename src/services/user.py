from fastapi import Depends

from db.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_user_id(self, login: str) -> int:
        user_id = await self.user_repo.get_id_by_login(login=login)
        return user_id

    async def get_login_by_id(self, id_user: int) -> str:
        login = await self.user_repo.get_login_by_id(user_id=id_user)
        return login
