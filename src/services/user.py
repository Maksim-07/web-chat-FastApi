import jwt
from fastapi import Depends, Request
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import credentials_exception, invalid_token_exception
from db.repository.user import UserRepository
from schemas.users import CurrentUserSchema


class UserService:
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

            user_schema = CurrentUserSchema(id=user_id, login=login)
        except InvalidTokenError:
            raise invalid_token_exception

        return user_schema
