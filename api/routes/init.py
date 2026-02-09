import logging

from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.init import Request as InitRequest
from api.services.sessions import generate_session_id, hash_key
from database import get_session_generator
from database.models import Session, User
from loader import bot

router = APIRouter(prefix="/init")


@router.post("")
async def _init(request: Request, response: Response, body: InitRequest = None, session: AsyncSession = Depends(get_session_generator)):
    logger = request.app.state.logger
    if not body:
        raise HTTPException(400, "invalid_request")

    try:
        data = safe_parse_webapp_init_data(bot.token, init_data=body.init_data)
    except Exception:
        raise HTTPException(400, "invalid_request")

    user = await User.get(data.user.id, session=session)
    if not user:
        raise HTTPException(400, "invalid_request")

    session_id = generate_session_id()
    await Session.create(key=hash_key(session_id.encode()), user_id=user.id, session=session)
    await session.commit()
    logger.info(f"[user_id]: {user.id} — authorized")

    response.set_cookie("session_id", session_id, samesite="none", secure=True, httponly=True)
    return "ok"
