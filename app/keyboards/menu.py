from aiogram.types import KeyboardButton, WebAppInfo

from app.keyboards.base import BaseReplyKeyboard
from loader import _


class MenuKeyboard(BaseReplyKeyboard):
    @classmethod
    def buttons(cls):
        return [
            KeyboardButton(text=_("Add word")),
            KeyboardButton(text=_("Dictionaries")),
        ]
