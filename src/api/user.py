from fastapi import APIRouter, Depends, Request

from schemas.users import CurrentUserSchema
from services.auth import AuthService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=CurrentUserSchema)
async def get_current_user(request: Request, auth_service: AuthService = Depends()) -> CurrentUserSchema:
    return await auth_service.get_current_user(request=request)
