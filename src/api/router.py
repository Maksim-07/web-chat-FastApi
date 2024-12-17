from fastapi import APIRouter, Depends

from api.auth import router as auth_router
from api.user import router as user_router
from api.websocket import router as websocket_router
from core.auth import verify_token_from_query, verify_token_from_header

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(websocket_router, dependencies=[Depends(verify_token_from_query)])
router.include_router(websocket_router)
router.include_router(user_router, dependencies=[Depends(verify_token_from_header)])
