import random

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import current_user
from api.models.words import Response as WordResponse
from database import get_session_generator
from database.models import User, Word

router = APIRouter(prefix="/words", dependencies=[])


@router.get("", response_model=list[WordResponse])
async def _words(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return sorted([w.to_dict() for w in current_user.words], key=lambda w: w["id"])


@router.get("/random", response_model=WordResponse)
async def _random_word(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return random.choice(current_user.words).to_dict() if current_user.words else None


@router.delete("/{id}")
async def _remove_word(
    id: int,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session_generator),
):
    await current_user.awaitable_attrs.words

    word = await Word.get_by(Word.id == id, Word.user_id == current_user.id, session=session)
    await session.delete(word)
    await session.commit()

    return "ok"
