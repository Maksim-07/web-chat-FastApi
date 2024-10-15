from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from api.static import templates
from schemas.users import UserAuthSchema, UserRegisterSchema
from services.user import UserService

auth_router = APIRouter(prefix="/auth", tags=["Authorization"])


@auth_router.get("", response_class=HTMLResponse)
async def get_window_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@auth_router.post("/login")
async def login_user(user_scheme: UserAuthSchema, auth_service: UserService = Depends()):
    return await auth_service.login(user_scheme)


@auth_router.post("/register")
async def register_user(user_scheme: UserRegisterSchema, user_service: UserService = Depends()):
    return await user_service.register(user_scheme)
