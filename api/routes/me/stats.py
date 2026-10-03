from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.depends import current_user
from surreal.base import current_session
from surreal.models import Know, User

router = APIRouter(prefix="/stats", dependencies=[])


class Day(BaseModel):
    date: datetime
    total: int
    success: int
    failure: int


@router.get("")
async def _stats(current_user: User = Depends(current_user)):
    session = current_session.get()
    user_words = [Know.model_validate(w) for w in await session.query(f"SELECT * FROM know WHERE in = {current_user.id}")]

    count = len(user_words)
    reviewed = list(filter(lambda w: w.last_reviewed_at, user_words))
    avg_streak = round(sum(word.repetitions for word in reviewed) / len(reviewed) if len(reviewed) > 0 else 0, 1)

    now = datetime.now(UTC)
    due_words = list(filter(lambda w: w.due_at is not None and w.due_at <= now, user_words))

    difficult_words = list(filter(lambda w: w.ease_factor < 2.0, user_words))

    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=6)
    week = await session.query(f"""SELECT
        count() AS total,
        count(IF quality < 3 THEN 1 END) AS failure,
        count(IF quality >= 3 THEN 1 END) AS success,
        time::group(reviewed_at, 'day') AS date
    FROM review WHERE in = {current_user.id} AND reviewed_at >= d'{week_start.isoformat()}' 
    GROUP BY date""")
    stats_by_date = {d["date"].date(): d for d in week}
    week = [
        {
            "date": datetime.combine(day, datetime.min.time(), tzinfo=UTC),
            "total": stats_by_date.get(day, {}).get("total", 0),
            "failure": stats_by_date.get(day, {}).get("failure", 0),
            "success": stats_by_date.get(day, {}).get("success", 0),
        }
        for i in range(7)
        if (day := (week_start + timedelta(days=i)).date())
    ]

    return {
        "words_count": count,
        "avg_streak": avg_streak,
        "due_words_count": len(due_words),
        "difficult_words_count": len(difficult_words),
        "week": [Day.model_validate(d) for d in week],
    }
