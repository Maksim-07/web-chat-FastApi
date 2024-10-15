from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.exceptions import (
    incorrect_login_or_password_exception,
    user_already_exists_exception,
)
from db.repository.user import UserRepository
from schemas.users import UserAuthSchema, UserRegisterSchema
from services.password import PasswordService

router = APIRouter(prefix="/auth", tags=["Authorization"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_window_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/login/")
async def login_user(user_scheme: UserAuthSchema, password_service: PasswordService = Depends()):
    user = await password_service.authenticate_user(login=user_scheme.login, password=user_scheme.password)
    if user is None:
        raise incorrect_login_or_password_exception
    return {"ok": True, "message": "Авторизация успешна"}


@router.post("/register")
async def register_user(user_scheme: UserRegisterSchema, user_repo: UserRepository = Depends()):
    login = user_scheme.login
    password = user_scheme.password

    hashed_password = PasswordService().get_password_hash(password=password)

    user = await user_repo.find(login=login)
    if user:
        raise user_already_exists_exception

    await user_repo.add(login=login, password=hashed_password)
    return {"message": "Зарегистрирован"}
