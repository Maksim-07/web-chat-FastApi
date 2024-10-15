from fastapi import APIRouter

from api.auth import auth_router
from api.chat import chat_router
from api.static import static_router

router = APIRouter(prefix="")

router.include_router(static_router)
router.include_router(auth_router)
router.include_router(chat_router)
