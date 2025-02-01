from fastapi import APIRouter

from .cards import router as cards_router
from .words import router as words_router

router = APIRouter()
router.include_router(cards_router, prefix="/cards")
router.include_router(words_router, prefix="/words")
