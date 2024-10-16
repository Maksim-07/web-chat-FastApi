from fastapi import APIRouter

from api.auth import router as auth_router
from api.chat import router as chat_router
from api.static import router as static_router

router = APIRouter(prefix="")

router.include_router(static_router)
router.include_router(auth_router)
router.include_router(chat_router)
