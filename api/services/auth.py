import json
import random
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Cookie

from api.schemas import WordResponse
from database import get_session
from database.models import User
from loader import redis_sessions


async def start_user_session(user_id: int) -> str:
    expire_at = datetime.now(timezone.utc).replace(hour=4, minute=0, second=0, microsecond=0) + timedelta(days=1)
    if not await redis_sessions.exists(f"session:{user_id}"):
        words = []
        async with get_session() as session:
            user = await User.get(user_id, session=session)
            dictionaries = await user.get_dictionaries()
            for i in dictionaries:
                words.extend([WordResponse.model_validate(w).model_dump() for w in await i.get_words()])
        random.shuffle(words)
        await redis_sessions.hset(f"session:{user_id}", "words", json.dumps(words))
        await redis_sessions.expireat(f"session:{user_id}", expire_at)
    return jwt.encode({"user_id": user_id, "exp": expire_at}, "secret_key", algorithm="HS256")


async def get_user_session(token: str) -> dict | None:
    try:
        user_id = jwt.decode(token, "secret_key", algorithms=["HS256"])["user_id"]
    except:
        return None
    if not await redis_sessions.exists(f"session:{user_id}"):
        return None
    data = {}
    for key, value in (await redis_sessions.hgetall(f"session:{user_id}")).items():
        data[key.decode("utf-8")] = json.loads(value.decode("utf-8"))
    return data


async def get_current_user(session=Cookie(...)):
    user = await get_user_session(session)
    return user
