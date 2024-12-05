from fastapi import APIRouter, Depends, WebSocket

from services.message import MessageService

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, message_service: MessageService = Depends()) -> None:
    await message_service.process_websocket(websocket=websocket, client_id=client_id)
