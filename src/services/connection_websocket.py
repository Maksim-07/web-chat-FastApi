import functools
from typing import List

import jwt
from fastapi import Depends, Query, WebSocket
from jwt import InvalidTokenError

from core.config import settings
from core.exceptions import (
    credentials_exception,
    invalid_token_exception,
    token_not_found_exception,
    user_not_found_exception,
)
from db.repository.user import UserRepository
from schemas.message import CurrentMessageSchema


async def get_and_verify_token_from_query(
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


class ConnectionManagerService:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: CurrentMessageSchema, websocket: WebSocket) -> None:
        await websocket.send_json(message.model_dump_json())

    async def broadcast(self, message: CurrentMessageSchema, websocket: WebSocket) -> None:
        for connection in self.active_connections:
            if connection == websocket:
                continue
            await connection.send_json(message.model_dump_json())


@functools.lru_cache()
def connection_manager() -> ConnectionManagerService:
    return ConnectionManagerService()
