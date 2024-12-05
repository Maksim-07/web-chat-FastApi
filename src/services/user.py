import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from core.config import settings
from core.exceptions import credentials_exception, invalid_token_exception
from db.repository.user import UserRepository
from schemas.token import TokenData
from schemas.users import UserIdSchema, UserLoginSchema


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    @staticmethod
    async def get_current_user(token) -> TokenData:
        try:
            payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
            login: str = payload.get("sub")
            if login is None:
                raise credentials_exception
            token_data = TokenData(login=login)
        except InvalidTokenError:
            raise invalid_token_exception

        return token_data

    async def get_user_id(self, login: str) -> UserIdSchema:
        user_id = await self.user_repo.get_id_by_login(login=login)

        return UserIdSchema(id=user_id)

    async def get_user_login(self, id_user: int) -> UserLoginSchema:
        login = await self.user_repo.get_login_by_id(user_id=id_user)

        return UserLoginSchema(login=login)
