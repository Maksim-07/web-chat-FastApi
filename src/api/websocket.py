from functools import lru_cache

from fastapi import APIRouter, Depends, WebSocket

from services.connection_websocket import ConnectionManagerService, connection_manager
from services.message import MessageService

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    message_service: MessageService = Depends(),
    connection: ConnectionManagerService = Depends(lru_cache(connection_manager)),
) -> None:
    await message_service.process_websocket(websocket, client_id, connection)
