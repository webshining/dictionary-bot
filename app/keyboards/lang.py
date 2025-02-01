from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from loader import i18n
from .base import BaseInlineKeyboard


class LangKeyboard(BaseInlineKeyboard, CallbackData, prefix="lang"):
    lang: str

    @staticmethod
    def buttons():
        return [InlineKeyboardButton(text=lang.upper(), callback_data=LangKeyboard(lang=lang).pack()) for lang in
                i18n.available_locales]
