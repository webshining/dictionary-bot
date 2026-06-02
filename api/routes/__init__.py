from fastapi import APIRouter

from .me import router as me_router

router = APIRouter(prefix="/api")
router.include_router(me_router)
