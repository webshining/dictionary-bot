from fastapi import APIRouter

from .auth import router as auth_router
from .cards import router as cards_router

router = APIRouter()
router.include_router(cards_router, prefix="/cards")
router.include_router(auth_router, prefix="/auth")
