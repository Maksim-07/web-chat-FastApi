from fastapi import APIRouter, status
from fastapi.params import Depends

from schemas.message import MessageSchema
from services.message import MessageService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/send_message", status_code=status.HTTP_200_OK)
async def send_message(message: MessageSchema, message_service: MessageService = Depends()):
    return await message_service.send_message(message)


@router.get("/read_message", status_code=status.HTTP_200_OK)
async def read_message(login: str, message_service: MessageService = Depends()):
    return await message_service.read_message(login)
