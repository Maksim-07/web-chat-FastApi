from fastapi import APIRouter, status

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("", status_code=status.HTTP_200_OK)
async def login_to_chat():
    return {"login": True}
