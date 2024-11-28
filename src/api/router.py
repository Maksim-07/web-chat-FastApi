from fastapi import APIRouter

from api.auth import router as auth_router
from api.static import router as static_router
from api.user import router as user_router
from api.websocket import router as websocket_router

router = APIRouter(prefix="")

router.include_router(static_router)
router.include_router(auth_router)
router.include_router(websocket_router)
router.include_router(user_router)
