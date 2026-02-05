import logging
from datetime import datetime, timezone
from typing import Annotated

from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.init import Request
from api.services.sessions import generate_session_id, hash_key
from database import get_session_generator
from database.models import Session, User
from loader import bot

router = APIRouter(prefix="/init")


@router.post("")
async def _init(
    response: Response,
    body: Request = None,
    session: AsyncSession = Depends(get_session_generator),
    session_id: Annotated[str | None, Cookie()] = None,
):
    logger = logging.getLogger("uvicorn")
    if not body:
        raise HTTPException(400, "invalid_request")

    try:
        data = safe_parse_webapp_init_data(bot.token, init_data=body.init_data)
        if not data.query_id:
            raise HTTPException(400, "invalid_request")
    except Exception:
        raise HTTPException(400, "invalid_request")

    if session_id and (
        user_session := await Session.get_by(
            Session.key == hash_key(session_id.encode()), Session.expired_at > datetime.now(timezone.utc), session=session
        )
    ):
        if data.query_id == user_session.query_id:
            user_session.refresh()
            logger.info(
                f"[user_id]: {(await user_session.awaitable_attrs.user).id} [query_id]: {data.query_id} [session_id]: {session_id} — refreshed"
            )
        else:
            user_session.revoke()
            f"[user_id]: {(await user_session.awaitable_attrs.user).id} [query_id]: {data.query_id} [session_id]: {session_id} — revoked"
        await session.commit()

        return "ok"

    user = await User.get(data.user.id, session=session)
    if not user:
        raise HTTPException(400, "invalid_request")

    session_id = generate_session_id()
    user_session = await Session.create(query_id=data.query_id, key=hash_key(session_id.encode()), user_id=user.id, session=session)
    await session.commit()
    logger.info(f"[user_id]: {user.id} [query_id]: {data.query_id} [session_id]: {session_id} — created")

    response.set_cookie("session_id", session_id, samesite="none", secure=True, httponly=True)
    return "ok"
