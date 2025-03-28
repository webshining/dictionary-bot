from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, WebAppInfo

from data.config import WEB_APP_URL
from loader import _

from .base import BaseInlineKeyboard


class DictionaryKeyboard(BaseInlineKeyboard, CallbackData, prefix="dictionary"):
    id: int
    action: str

    @staticmethod
    def buttons(id: int):
        return [
            InlineKeyboardButton(text=_("Cards"), web_app=WebAppInfo(url=f"{WEB_APP_URL}/cards/{id}/init")),
            InlineKeyboardButton(
                text=_("View"),
                web_app=WebAppInfo(url=f"{WEB_APP_URL}/dictionaries/{id}/init"),
            ),
            InlineKeyboardButton(text=_("Delete"), callback_data=DictionaryKeyboard(id=id, action="delete").pack()),
        ]
