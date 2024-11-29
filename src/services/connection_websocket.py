from typing import List

from fastapi import WebSocket


class ConnectionManagerService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: dict[str, str], websocket: WebSocket) -> None:
        await websocket.send_json(message)

    async def broadcast(self, message: dict[str, str], websocket: WebSocket) -> None:
        for connection in self.active_connections:
            if connection == websocket:
                continue
            await connection.send_json(message)


connection_manager: ConnectionManagerService = ConnectionManagerService()
