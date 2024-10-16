from fastapi import APIRouter, Depends, status

from schemas.users import UserAuthSchema, UserRegisterSchema
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_scheme: UserAuthSchema, auth_service: AuthService = Depends()):
    return await auth_service.login(user_scheme)


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user_scheme: UserRegisterSchema, user_service: AuthService = Depends()):
    return await user_service.register(user_scheme)
