from fastapi import Depends

from db.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_user_id(self, login) -> int:
        user_id = await self.user_repo.get_id_by_login(login=login)
        return user_id
