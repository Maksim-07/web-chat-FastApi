from functools import lru_cache
from typing import Sequence

from fastapi import Depends, WebSocket, WebSocketDisconnect

from core.exceptions import id_not_found_exception, login_not_found_exception
from db.repository.message import MessageRepository
from db.repository.user import UserRepository
from schemas.message import CurrentMessageSchema, MessageSchema
from services.connection_websocket import ConnectionManagerService, connection_manager
from services.user import UserService


class MessageService:
    def __init__(
        self,
        message_repo: MessageRepository = Depends(),
        user_repo: UserRepository = Depends(),
        user_service: UserService = Depends(),
    ):
        self.message_repo = message_repo
        self.user_repo = user_repo
        self.user_service = user_service

    async def add_message(self, message: MessageSchema) -> None:
        await self.message_repo.add(sender_id=message.sender_id, message=message.message)

    async def get_messages(self, login) -> Sequence[str]:
        user_id = await self.user_repo.get_id_by_login(login=login)

        if not user_id:
            raise id_not_found_exception

        return await self.message_repo.get_messages_by_sender_id(user_id)

    async def process_websocket(
        self,
        websocket: WebSocket,
        client_id: int,
        connection: ConnectionManagerService = Depends(lru_cache(connection_manager)),
    ) -> None:
        await connection.connect(websocket)

        user_name = await self.user_repo.get_login_by_id(user_id=client_id)

        if not user_name:
            raise login_not_found_exception

        all_messages = await self.message_repo.get_all_messages()
        for m in all_messages:
            message = CurrentMessageSchema(login=m[0], message=m[1])
            await connection.send_personal_message(message, websocket)

        connect_message = CurrentMessageSchema(message=f"{user_name} присоединился(-лась) к чату")
        disconnect_message = CurrentMessageSchema(message=f"{user_name} вышел(-ла) из чата")

        await connection.broadcast(connect_message, websocket)

        try:
            while True:
                data = await websocket.receive_text()

                message = CurrentMessageSchema(login=user_name, message=data)

                await connection.send_personal_message(message, websocket)

                await connection.broadcast(message, websocket)

                await self.add_message(MessageSchema(sender_id=client_id, message=data))

        except WebSocketDisconnect:
            connection.disconnect(websocket)

            await connection.broadcast(disconnect_message, websocket)
