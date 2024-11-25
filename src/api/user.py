from fastapi import APIRouter, Depends

from services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/id")
async def get_id(login: str, user_service: UserService = Depends()):
    return await user_service.get_user_id(login=login)
