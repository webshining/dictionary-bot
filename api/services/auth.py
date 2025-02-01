from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from fastapi import Header, HTTPException

from data.config import TELEGRAM_BOT_TOKEN
from database.models import User


async def get_current_user(initData: str = Header(...)) -> User:
    if not check_webapp_signature(TELEGRAM_BOT_TOKEN, initData):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return safe_parse_webapp_init_data(TELEGRAM_BOT_TOKEN, initData).user.id
