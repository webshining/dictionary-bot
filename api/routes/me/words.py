import random

from fastapi import APIRouter, Depends

from api.depends import current_user
from api.models.words import Response as WordResponse
from database import get_session_generator
from database.models import User

router = APIRouter(prefix="/words", dependencies=[Depends(get_session_generator)])


@router.get("", response_model=list[WordResponse])
async def _words(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return sorted([w.to_dict() for w in current_user.words], key=lambda w: w["id"])


@router.get("/random", response_model=WordResponse)
async def _random_word(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return random.choice(current_user.words).to_dict() if current_user.words else None
