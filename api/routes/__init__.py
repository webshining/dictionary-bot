from fastapi import APIRouter

from .cards import router as cards_router
from .dictionaries import router as dictionaries_router
from .words import router as words_router

router = APIRouter()
router.include_router(cards_router, prefix="/cards")
router.include_router(dictionaries_router, prefix="/dictionaries")
router.include_router(words_router, prefix="/words")
