from fastapi import APIRouter, Depends

from core.auth import oauth2_scheme
from schemas.users import CurrentUserSchema
from services.user import UserService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=CurrentUserSchema)
async def get_current_user(
    token: str = Depends(oauth2_scheme), user_service: UserService = Depends()
) -> CurrentUserSchema:
    return await user_service.get_current_user(token=token)
