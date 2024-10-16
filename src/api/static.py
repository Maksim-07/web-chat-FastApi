from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="")


@router.get("/", status_code=status.HTTP_200_OK)
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@router.get("/auth", status_code=status.HTTP_200_OK)
async def get_window_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})
