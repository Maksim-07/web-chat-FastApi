from fastapi import APIRouter

chat_router = APIRouter(prefix="/chat", tags=["Chat"])


@chat_router.get("")
async def login_to_chat():
    return {"login": True}
