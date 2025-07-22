from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

from bot.text import Text


class DictionaryKeyboard(CallbackData, prefix="dictionary"):
    id: int
    action: str

    @staticmethod
    def keyboard(id: int):
        builder = InlineKeyboardBuilder()
        buttons = [
            InlineKeyboardButton(
                text=str(Text.VIEW_BUTTON),
                web_app=WebAppInfo(url=f"{settings.FRONTEND_URL}/dictionaries/{id}"),
            ),
        ]
        builder.add(*buttons)
        return builder.as_markup()
