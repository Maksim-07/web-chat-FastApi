from fastapi import APIRouter, Depends, Request

from schemas.users import CurrentUserSchema
from services.user import UserService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=CurrentUserSchema)
async def get_current_user(request: Request, user_service: UserService = Depends()) -> CurrentUserSchema:
    return await user_service.get_current_user(request=request)
