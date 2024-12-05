from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from passlib.context import CryptContext

from core.config import settings
from core.exceptions import (
    incorrect_password_exception,
    user_already_exists_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository
from schemas.token import TokenSchema
from schemas.users import UserAuthSchema, UserRegisterSchema


class AuthService:
    __ctx = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key=settings().SECRET_KEY, algorithm=settings().ALGORITHM)

        return encoded_jwt

    async def login(self, user: UserAuthSchema) -> TokenSchema:
        current_user = await self.user_repo.get_by(login=user.login)

        if not current_user:
            raise user_not_found_exception

        if self.__verify_password(password=user.password, hash_password=current_user.password):
            access_token_expires = timedelta(minutes=settings().ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"sub": current_user.login}, expires_delta=access_token_expires
            )

            return TokenSchema(access_token=access_token, token_type="bearer")

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
