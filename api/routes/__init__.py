from fastapi import APIRouter

from .words import router as words_router

router = APIRouter(prefix="/api")
router.include_router(words_router)
