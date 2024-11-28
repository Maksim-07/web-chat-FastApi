from typing import Sequence

from fastapi import Depends, WebSocket, WebSocketDisconnect

from db.repository.message import MessageRepository
from db.repository.user import UserRepository
from schemas.message import MessageSchema
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

    async def send_message(self, message: MessageSchema) -> None:
        await self.message_repo.add(sender_id=message.sender_id, message=message.message)

    async def read_message(self, login) -> Sequence[str]:
        user_id = await self.user_repo.get_id_by_login(login=login)

        return await self.message_repo.get_message_by_sender_id(user_id)

    async def show_all_messages(self) -> list[dict[str, str]]:
        all_messages = await self.message_repo.get_all()

        list_messages = []
        for message in all_messages:
            dict_message: dict[str, str] = {}

            user_id = message.sender_id
            login = await self.user_service.get_login_by_id(user_id)

            dict_message["sender_id"] = login
            dict_message["message"] = message.message

            list_messages.append(dict_message)

        return list_messages

    async def working_with_websocket(self, websocket: WebSocket, client_id: int):
        await connection_manager.connect(websocket)

        user_name = await self.user_repo.get_login_by_id(user_id=client_id)

        all_messages = await self.show_all_messages()
        for message in all_messages:
            await connection_manager.send_personal_message(f"{message["sender_id"]}: {message["message"]}", websocket)

        await connection_manager.broadcast(f"{user_name} присоединился к чату", websocket)

        try:
            while True:
                data = await websocket.receive_text()

                await connection_manager.send_personal_message(f"Вы: {data}", websocket)

                await connection_manager.broadcast(f"{user_name}: {data}", websocket)

                await self.send_message(MessageSchema(sender_id=client_id, message=data))

        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)

            await connection_manager.broadcast(f"{user_name} вышел из чата", websocket)
