from typing import Annotated

from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.init import Request
from api.models.init import Response as InitResponse
from api.services.sessions import generate_session_keys, hash_key
from database import get_session_generator
from database.models import Session, User
from loader import bot

router = APIRouter(prefix="/init")


@router.post(
    "",
    response_model=InitResponse,
)
async def _init(
    response: Response,
    body: Request,
    session: AsyncSession = Depends(get_session_generator),
    session_id: Annotated[str | None, Cookie()] = None,
) -> InitResponse:
    try:
        data = safe_parse_webapp_init_data(bot.token, init_data=body.init_data)
    except Exception:
        raise HTTPException(400, "invalid_request")

    user = await User.get(data.user.id, session=session)
    if not user:
        raise HTTPException(400, "invalid_request")

    user_session = await Session.get_by(Session.user_id == user.id, Session.query_id == data.query_id, session=session)
    if user_session:
        if session_id and hash_key(session_id.encode()) == user_session.key:
            await user_session.awaitable_attrs.user
            await user_session.user.awaitable_attrs.languages
            return user_session.user
        else:
            raise HTTPException(409, "already_authorized")

    session_id, session_key = generate_session_keys()
    user_session = await Session.create(query_id=data.query_id, key=session_key, user_id=user.id, session=session)
    await session.commit()

    response.set_cookie("session_id", session_id, expires=user_session.expired_at, samesite="none", secure=True, httponly=True)

    await user.awaitable_attrs.languages
    return user
