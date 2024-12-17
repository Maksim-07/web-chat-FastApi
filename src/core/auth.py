import jwt
from fastapi import Depends, Query, Request
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import (
    credentials_exception,
    invalid_token_exception,
    token_not_found_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository


async def verify_token_from_header(request: Request, user_repo: UserRepository = Depends()) -> None:
    token = request.headers.get("Authorization")
    try:
        payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        user = await user_repo.get_by(id=user_id)
        if user is None:
            raise user_not_found_exception

    except InvalidTokenError:
        raise invalid_token_exception


async def verify_token_from_query(
    token: str = Query(None, alias="token"), user_repo: UserRepository = Depends()
) -> None:
    if not token:
        raise token_not_found_exception

    try:
        payload = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        user = await user_repo.get_by(id=user_id)
        if user is None:
            raise user_not_found_exception

    except InvalidTokenError:
        raise invalid_token_exception
