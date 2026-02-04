from fastapi import APIRouter

from .init import router as init_router
from .words import router as words_router

router = APIRouter(prefix="/api")
router.include_router(init_router)
router.include_router(words_router)
