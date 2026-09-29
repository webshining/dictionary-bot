import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from data.config import TELEGRAM_BOT_TOKEN
from surreal.models import User

security = HTTPBearer()


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials.credentials:
        return None

    try:
        claims = jwt.decode(credentials.credentials, TELEGRAM_BOT_TOKEN, ["HS256"], verify=True)
    except:
        return None

    db = request.app.state.database
    user = User.model_validate(await db.query(f"SELECT * FROM ONLY user:{claims['sub']}"))

    return user


async def current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    current_user = await get_current_user(request, credentials)
    if not current_user:
        raise HTTPException(401, "unauthorized")

    return current_user
