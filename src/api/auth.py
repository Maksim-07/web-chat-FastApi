from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.token import TokenSchema
from schemas.users import UserRegisterSchema
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def login_user(user: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()) -> TokenSchema:
    return await auth_service.login(user=user)


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user: UserRegisterSchema, auth_service: AuthService = Depends()) -> None:
    return await auth_service.register(user=user)
