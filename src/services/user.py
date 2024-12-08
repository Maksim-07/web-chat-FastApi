import jwt
from fastapi import Depends
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import credentials_exception, invalid_token_exception
from db.repository.user import UserRepository
from schemas.token import TokenDataSchema


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    @staticmethod
    async def get_current_user(token: str) -> TokenDataSchema:
        try:
            payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
            user_id: str = payload.get("id")
            login: str = payload.get("login")
            if user_id is None:
                raise credentials_exception
            token_data = TokenDataSchema(id=user_id, login=login)
        except InvalidTokenError:
            raise invalid_token_exception

        return token_data
