from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

static_router = APIRouter(prefix="")


@static_router.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")
