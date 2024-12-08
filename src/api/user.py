from fastapi import APIRouter, Depends

from schemas.token import TokenDataSchema
from services.user import UserService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=TokenDataSchema)
async def get_current_user(token: str, user_service: UserService = Depends()) -> TokenDataSchema:
    return await user_service.get_current_user(token=token)
