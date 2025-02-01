from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from database.models import Dictionary
from loader import _
from .base import BaseInlineKeyboard


class DictionariesKeyboard(BaseInlineKeyboard, CallbackData, prefix="dictionaries"):
    data: str
    id: int = 0
    action: str = "0"

    @staticmethod
    def buttons(data: str, dictionaries: list[Dictionary] = []):
        return [
            *[InlineKeyboardButton(text=d.name, callback_data=DictionariesKeyboard(data=data, id=d.id).pack()) for d in
              dictionaries],
            InlineKeyboardButton(text=_("Create"),
                                 callback_data=DictionariesKeyboard(data=data, action="create").pack()),
            InlineKeyboardButton(text=_("Refresh"),
                                 callback_data=DictionariesKeyboard(data=data, action="refresh").pack())
        ]
