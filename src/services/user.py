import jwt
from fastapi import Depends, Request
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import (
    credentials_exception,
    invalid_token_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository
from schemas.users import CurrentUserSchema, UserBaseSchema


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_current_user(self, token: str) -> CurrentUserSchema:
        try:
            payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
            user_id: int = payload.get("user_id")

            if user_id is None:
                raise credentials_exception

            user = await self.get_user(user_id=user_id)
            if not user:
                raise user_not_found_exception

            user_schema = CurrentUserSchema(id=user.id, login=user.login)
        except InvalidTokenError:
            raise invalid_token_exception

        return user_schema

    async def get_user(self, user_id: int) -> UserBaseSchema:
        user = await self.user_repo.get_by(id=user_id)

        if not user:
            raise user_not_found_exception

        return UserBaseSchema(id=user.id, login=user.login, created_at=user.created_at, updated_at=user.updated_at)
