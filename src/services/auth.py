from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext

from core.config import settings
from core.exceptions import (
    credentials_exception,
    incorrect_password_exception,
    invalid_token_exception,
    user_already_exists_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository
from schemas.token import TokenDataSchema, TokenSchema
from schemas.users import CurrentUserSchema


class AuthService:
    __ctx = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    @staticmethod
    async def get_current_user(request: Request) -> CurrentUserSchema:
        token = request.headers.get("Authorization")
        try:
            payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
            user_id: int = payload.get("user_id")
            login: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = CurrentUserSchema(id=user_id, login=login)
        except InvalidTokenError:
            raise invalid_token_exception

        return token_data

    async def login(self, user: OAuth2PasswordRequestForm) -> TokenSchema:
        current_user = await self.user_repo.get_by(login=user.username)

        if not current_user:
            raise user_not_found_exception

        if self.__verify_password(password=user.password, hash_password=current_user.password):
            access_token = self.__create_access_token(
                data=CurrentUserSchema(id=current_user.id, login=current_user.login)
            )

            return TokenSchema(access_token=access_token, token_type="bearer")

        raise incorrect_password_exception

    async def register(self, login: str, password: str) -> None:
        current_user = await self.user_repo.get_by(login=login)

        if current_user:
            raise user_already_exists_exception

        hashed_password = self.__get_password_hash(password=password)
        await self.user_repo.add(login=login, password=hashed_password)

    def __get_password_hash(self, password: str) -> str:
        return self.__ctx.hash(password)

    def __verify_password(self, password: str, hash_password: str) -> bool:
        return self.__ctx.verify(password, hash_password)

    @staticmethod
    def __create_access_token(data: CurrentUserSchema) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings().ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = TokenDataSchema(user_id=data.id, sub=data.login, exp=expire)
        encoded_jwt = jwt.encode(to_encode.model_dump(), key=settings().SECRET_KEY, algorithm=settings().ALGORITHM)

        return encoded_jwt
