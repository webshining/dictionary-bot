from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from .base import BaseInlineKeyboard


class ApplyKeyboard(BaseInlineKeyboard, CallbackData, prefix="apply"):
    data: str

    @staticmethod
    def buttons(data: str):
        return [InlineKeyboardButton(text="🆗", callback_data=ApplyKeyboard(data=data).pack())]
