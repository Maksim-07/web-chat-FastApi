from fastapi import APIRouter, Depends

from services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/id/{login}")
async def get_id(login: str, user_service: UserService = Depends()):
    user_id = await user_service.get_user_id(login=login)
    return {"id": user_id}


@router.get("/login/{user_id}")
async def get_id(user_id: int, user_service: UserService = Depends()):
    login = await user_service.get_login_by_id(id_user=user_id)
    return {"login": login}
