from fastapi import Depends
from passlib.context import CryptContext

from core.exceptions import (
    incorrect_password_exception,
    user_already_exists_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository
from schemas.users import UserAuthSchema, UserBaseSchema, UserRegisterSchema


class AuthService:
    __ctx = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def login(self, user: UserAuthSchema) -> None:
        current_user = await self.user_repo.get_by(login=user.login)

        if not current_user:
            raise user_not_found_exception

        if self.__verify_password(password=user.password, hash_password=current_user.password):
            return
        raise incorrect_password_exception

    async def register(self, user: UserRegisterSchema) -> None:
        current_user = await self.user_repo.get_by(login=user.login)

        if current_user:
            raise user_already_exists_exception

        hashed_password = self.__get_password_hash(password=user.password)
        await self.user_repo.add(login=user.login, password=hashed_password)

    def __get_password_hash(self, password: str) -> str:
        return self.__ctx.hash(password)

    def __verify_password(self, password: str, hash_password: str) -> bool:
        return self.__ctx.verify(password, hash_password)
