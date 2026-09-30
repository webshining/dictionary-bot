from fastapi import APIRouter, Depends, HTTPException

from api.depends import current_user
from api.models.words import ReviewRequest
from surreal.base import current_session
from surreal.models import Know, User

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
    id: str,
    current_user: User = Depends(current_user),
):
    session = current_session.get()
    await session.query(f"DELETE know WHERE id = know:{id} AND in = {current_user.id}")
    return "ok"
