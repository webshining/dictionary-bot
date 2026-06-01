import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import TELEGRAM_BOT_TOKEN
from database import get_session_generator
from database.models import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_generator),
):
    if not credentials.credentials:
        return None

    try:
        claims = jwt.decode(credentials.credentials, TELEGRAM_BOT_TOKEN, ["HS256"], verify=True)
    except:
        return None

    user = await User.get_by(User.id == claims["userId"], session=session)

    return user


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_generator),
):
    current_user = await get_current_user(credentials, session)
    if not current_user:
        raise HTTPException(401, "unauthorized")

    return current_user
