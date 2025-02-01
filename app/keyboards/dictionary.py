from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, WebAppInfo

from loader import _

from .base import BaseInlineKeyboard


class DictionaryKeyboard(BaseInlineKeyboard, CallbackData, prefix="dictionary"):
    id: int
    action: str

    @staticmethod
    def buttons(id: int):
        return [
            InlineKeyboardButton(
                text=_("Cards"), web_app=WebAppInfo(url=f"https://calm-composed-gobbler.ngrok-free.app/cards/{id}")
            ),
            InlineKeyboardButton(
                text=_("View"), web_app=WebAppInfo(url=f"https://calm-composed-gobbler.ngrok-free.app/words/{id}")
            ),
            InlineKeyboardButton(text=_("Delete"), callback_data=DictionaryKeyboard(id=id, action="delete").pack()),
        ]
