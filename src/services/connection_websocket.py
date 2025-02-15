import functools
from typing import List

from fastapi import WebSocket

from schemas.message import CurrentMessageSchema


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
