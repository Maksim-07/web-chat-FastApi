from typing import Sequence

from fastapi import Depends, WebSocket, WebSocketDisconnect

from db.repository.message import MessageRepository
from db.repository.user import UserRepository
from schemas.message import CurrentMessageSchema, MessageSchema
from services.connection_websocket import connection_manager
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

        return await self.message_repo.get_messages_by_sender_id(user_id)

    async def get_list_messages(self) -> list[CurrentMessageSchema]:
        all_messages = await self.message_repo.get_all()

        list_messages = []
        for message in all_messages:
            user_id = message.sender_id
            login = await self.user_service.get_login_by_id(user_id)

            current_message = CurrentMessageSchema(sender=login, content=message.message)

            list_messages.append(current_message)

        return list_messages

    async def process_websocket(self, websocket: WebSocket, client_id: int) -> None:
        await connection_manager.connect(websocket)

        user_name = await self.user_repo.get_login_by_id(user_id=client_id)

        all_messages = await self.get_list_messages()
        for message in all_messages:
            m = message.model_dump_json()
            await connection_manager.send_personal_message(m, websocket)

        connect_message = CurrentMessageSchema(content=f"{user_name} присоединился(-лась) к чату").model_dump_json()
        disconnect_message = CurrentMessageSchema(content=f"{user_name} вышел(-ла) из чата").model_dump_json()

        await connection_manager.broadcast(connect_message, websocket)

        try:
            while True:
                data = await websocket.receive_text()

                message = CurrentMessageSchema(sender=user_name, content=data)

                await connection_manager.send_personal_message(message.model_dump_json(), websocket)

                await connection_manager.broadcast(message.model_dump_json(), websocket)

                await self.add_message(MessageSchema(sender_id=client_id, message=data))

        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)

            await connection_manager.broadcast(disconnect_message, websocket)
