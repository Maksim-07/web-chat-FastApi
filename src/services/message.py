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
        connection_manager_service: ConnectionManagerService = Depends(connection_manager),
    ):
        self.message_repo = message_repo
        self.user_repo = user_repo
        self.user_service = user_service
        self.connection_manager_service = connection_manager_service

    async def add_message(self, message: MessageSchema) -> None:
        await self.message_repo.add(sender_id=message.sender_id, message=message.message)

    async def get_messages(self, login) -> Sequence[str]:
        user_id = await self.user_repo.get_id_by_login(login=login)

        if not user_id:
            raise id_not_found_exception

        return await self.message_repo.get_messages_by_sender_id(user_id)

    async def process_websocket(self, websocket: WebSocket, client_id: int) -> None:
        await self.connection_manager_service.connect(websocket)

        user_name = await self.user_repo.get_login_by_id(user_id=client_id)

        if not user_name:
            raise login_not_found_exception

        all_messages = await self.message_repo.get_all_messages()
        for m in all_messages:
            message = CurrentMessageSchema(login=m[0], message=m[1])
            await self.connection_manager_service.send_personal_message(message, websocket)

        await self.connection_manager_service.broadcast(
            CurrentMessageSchema(message=f"{user_name} присоединился(-лась) к чату"), websocket
        )

        try:
            while True:
                data = await websocket.receive_text()

                message = CurrentMessageSchema(login=user_name, message=data)

                await self.connection_manager_service.send_personal_message(message, websocket)

                await self.connection_manager_service.broadcast(message, websocket)

                await self.add_message(MessageSchema(sender_id=client_id, message=data))

        except WebSocketDisconnect:
            self.connection_manager_service.disconnect(websocket)

            await self.connection_manager_service.broadcast(
                CurrentMessageSchema(message=f"{user_name} вышел(-ла) из чата"), websocket
            )
