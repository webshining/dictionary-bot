from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import current_user
from api.models.words import Response as WordResponse
from database import get_session_generator
from database.models import User, Word

router = APIRouter(prefix="/words", dependencies=[Depends(get_session_generator)])


@router.get("", response_model=list[WordResponse])
async def _words(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return [w.to_dict() for w in current_user.words]


@router.delete("/{id}")
async def _word_delete(id: int, current_user: User = Depends(current_user), session: AsyncSession = Depends(get_session_generator)):
    word = await Word.get_by(Word.user_id == current_user.id, Word.id == id, session=session)
    if word:
        await session.delete(word)
    return "ok"
