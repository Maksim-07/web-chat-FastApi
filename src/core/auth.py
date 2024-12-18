import jwt
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import (
    credentials_exception,
    invalid_token_exception,
    token_not_found_exception,
    user_not_found_exception,
)
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def verify_token(token: str, user_service: UserService) -> None:
    if not token:
        raise token_not_found_exception

    try:
        payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        user = await user_service.get_user(user_id)
        if not user:
            raise user_not_found_exception

    except InvalidTokenError:
        raise invalid_token_exception


async def verify_token_from_header(token: str = Depends(oauth2_scheme), user_service: UserService = Depends()) -> None:
    await verify_token(token=token, user_service=user_service)


async def verify_token_from_query(
    token: str = Query(None, alias="token"), user_service: UserService = Depends()
) -> None:
    await verify_token(token=token, user_service=user_service)
