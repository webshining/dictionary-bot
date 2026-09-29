from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import current_user
from api.models.words import ReviewRequest
from database import get_session_generator
from surreal.base import current_session
from surreal.models import Know, User, Word

router = APIRouter(prefix="/words", dependencies=[])


@router.get("", response_model=list[Know])
async def _words(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.words
    return current_user.words


@router.get("/cards", response_model=list[Know])
async def _study_cards(
    limit: int = 10,
    current_user: User = Depends(current_user),
):
    limit = min(max(limit, 1), 50)
    cards = await Know.get_study_cards(current_user.id, limit)
    return cards


@router.post("/{id}/review")
async def _review_word(
    id: str,
    review: ReviewRequest,
    current_user: User = Depends(current_user),
):
    session = current_session.get()
    if word := await session.query(f"SELECT * FROM ONLY know:{id} WHERE in = {current_user.id}"):
        word = Know.model_validate(word)
        await word.review(review.quality)
        return "ok"
    else:
        raise HTTPException(status_code=404, detail="word not found")


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
