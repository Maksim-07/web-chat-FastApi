import functools
from typing import List, Type

from fastapi import WebSocket


class ConnectionManagerService:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            print(type(cls.__instance))
        return cls.__instance

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    @functools.lru_cache()
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket) -> None:
        await websocket.send_json(message)

    async def broadcast(self, message: str, websocket: WebSocket) -> None:
        for connection in self.active_connections:
            if connection == websocket:
                continue
            await connection.send_json(message)


connection_manager: ConnectionManagerService = ConnectionManagerService()
