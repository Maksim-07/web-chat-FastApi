from fastapi import Depends
from passlib.context import CryptContext

from db.repository.user import UserRepository


class PasswordService:
    ctx = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    def get_password_hash(self, password: str) -> str:
        return self.ctx.hash(password)

    def verify_password(self, password: str, hash_password: str) -> bool:
        return self.ctx.verify(password, hash_password)

    async def authenticate_user(self, login, password):
        user = await self.user_repo.find(login=login)
        if not user or self.verify_password(password=password, hash_password=user.password) is False:
            return None
        return user
