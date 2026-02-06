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
        if not data.query_id:
            logger.info(f"[user_id]: {data.user.id} [query_id]: {data.query_id} — no_query_id")
            raise HTTPException(400, "invalid_request")
    except Exception:
        raise HTTPException(400, "invalid_request")

    user_session = await Session.get_by(Session.query_id == data.query_id)
    if user_session:
        logger.info(f"[user_id]: {(await user_session.awaitable_attrs.user).id} [query_id]: {data.query_id} — already_authorized")
        return "ok"

    user = await User.get(data.user.id, session=session)
    if not user:
        logger.info(f"[user_id]: {data.user.id} [query_id]: {data.query_id} — user_not_exist")
        raise HTTPException(400, "invalid_request")

    session_id = generate_session_id()
    user_session = await Session.create(query_id=data.query_id, key=hash_key(session_id.encode()), user_id=user.id, session=session)
    await session.commit()
    logger.info(f"[user_id]: {user.id} [query_id]: {data.query_id} — authorized")

    response.set_cookie("session_id", session_id, samesite="none", secure=True, httponly=True)
    return "ok"
