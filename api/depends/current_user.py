from datetime import datetime, timezone
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.sessions import hash_key
from database import get_session_generator
from database.models import Session


async def get_current_user(session: AsyncSession = Depends(get_session_generator), session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        return None

    key = hash_key(session_id.encode())
    user_session = await Session.get_by(Session.key == key, Session.expired_at > datetime.now(timezone.utc), session=session)
    if not user_session:
        return None

    return await user_session.awaitable_attrs.user


async def current_user(session: AsyncSession = Depends(get_session_generator), session_id: Annotated[str | None, Cookie()] = None):
    current_user = await get_current_user(session, session_id)
    if not current_user:
        raise HTTPException(401, "unauthorized")

    return current_user
