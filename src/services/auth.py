from fastapi import Depends
from passlib.context import CryptContext

from db.models import User
from db.repository.user import UserRepository


class AuthService:
    __ctx = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    def get_password_hash(self, password: str) -> str:
        return self.__ctx.hash(password)

    def __verify_password(self, password: str, hash_password: str) -> bool:
        return self.__ctx.verify(password, hash_password)

    async def authenticate_user(self, login: str, password: str) -> User | None:
        user = await self.user_repo.get_by(login=login)
        if not user or self.__verify_password(password=password, hash_password=user.password) is False:
            return None
        return user
