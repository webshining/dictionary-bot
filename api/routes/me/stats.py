from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from api.depends import current_user
from surreal.base import current_session
from surreal.models import Know, User

router = APIRouter(prefix="/stats", dependencies=[])


@router.get("")
async def _stats(current_user: User = Depends(current_user)):
    session = current_session.get()
    user_words = [Know.model_validate(w) for w in await session.query(f"SELECT * FROM know WHERE in = {current_user.id}")]

    count = len(user_words)
    reviewed = list(filter(lambda w: w.last_reviewed_at, user_words))
    avg_streak = sum(word.repetitions for word in reviewed) / len(reviewed) if len(reviewed) > 0 else 0

    now = datetime.now(UTC)
    due_words = list(filter(lambda w: w.due_at is not None and w.due_at <= now, user_words))

    difficult_words = list(filter(lambda w: w.ease_factor < 2.0, user_words))

    return {
        "words_count": count,
        "avg_streak": avg_streak,
        "due_words_count": len(due_words),
        "difficult_words_count": len(difficult_words),
    }
