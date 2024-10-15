from fastapi import Depends

from core.exceptions import (incorrect_login_or_password_exception,
                             user_already_exists_exception)
from db.repository.user import UserRepository
from schemas.users import UserAuthSchema, UserRegisterSchema
from services.auth import AuthService


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(), auth_service: AuthService = Depends()):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def login(self, user_scheme: UserAuthSchema):
        user = await self.auth_service.authenticate_user(login=user_scheme.login, password=user_scheme.password)
        if user is None:
            raise incorrect_login_or_password_exception
        return {"ok": True, "message": "Авторизация успешна"}

    async def register(self, user_scheme: UserRegisterSchema):
        login = user_scheme.login
        user = await self.user_repo.get_by(login=login)
        if user:
            raise user_already_exists_exception
        password = user_scheme.password

        hashed_password = self.auth_service.get_password_hash(password=password)

        await self.user_repo.add(login=login, password=hashed_password)
        return {"message": "Зарегистрирован"}
