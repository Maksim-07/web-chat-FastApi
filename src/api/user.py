from fastapi import APIRouter, Depends

from schemas.users import UserIdSchema
from services.message import MessageService
from services.user import UserService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/{login}", response_model=UserIdSchema)
async def get_id(login: str, user_service: UserService = Depends()) -> UserIdSchema:
    return await user_service.get_user_id(login=login)


# @router.get("/all-message")
# async def get_mess(message: MessageService = Depends()):
#     return await message.get_all_messages()
