import jwt
from fastapi import Query

from core.config import settings
from core.exceptions import invalid_token_exception, token_not_found_exception, credentials_exception
from schemas.users import CurrentUserSchema


def get_and_verify_token_from_query(token: str = Query(None, alias="token")) -> CurrentUserSchema:
    if not token:
        raise token_not_found_exception

    try:
        payload = jwt.decode(token, settings().SECRET_KEY, settings().ALGORITHM)
        user_id: int = payload.get("user_id")
        login: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_schema = CurrentUserSchema(id=user_id, login=login)

    except jwt.InvalidTokenError:
        raise invalid_token_exception

    return user_schema

