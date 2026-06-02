from fastapi import APIRouter

from .languages import router as languages_router
from .words import router as words_router

router = APIRouter(prefix="/me")
router.include_router(words_router)
router.include_router(languages_router)
