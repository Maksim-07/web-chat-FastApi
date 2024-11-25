from fastapi import Depends, WebSocket, WebSocketDisconnect

from db.repository.message import MessageRepository
from db.repository.user import UserRepository
from schemas.message import MessageSchema
from services.connection_websocket import connection_manager


class MessageService:
    def __init__(self, message_repo: MessageRepository = Depends(), user_repo: UserRepository = Depends()):
        self.message_repo = message_repo
        self.user_repo = user_repo

    async def send_message(self, message: MessageSchema) -> None:
        await self.message_repo.add(sender_id=message.sender_id, message=message.message)

    async def read_message(self, login):
        user_id = await self.user_repo.get_id_by_login(login=login)

        return await self.message_repo.get_message_by_sender_id(user_id)

    async def working_with_websocket(self, websocket: WebSocket, client_id: int):
        await connection_manager.connect(websocket)
        # user_name = await self.user_repo.get_login_by_id(user_id=client_id)
        try:
            while True:
                data = await websocket.receive_text()

                await connection_manager.send_personal_message(f"Вы: {data}", websocket)

                await connection_manager.broadcast(f"Клиент #{client_id}: {data}", websocket)
                # await connection_manager.broadcast(f"{user_name}: {data}", websocket)

        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)
            await connection_manager.broadcast(f"Клиент #{client_id} вышел из чата", websocket)
