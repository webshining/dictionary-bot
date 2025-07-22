from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

from bot.text import Text
from dictionary.models import Dictionary


class DictionariesKeyboard(CallbackData, prefix="dictionary"):
    id: int
    data: str

    @staticmethod
    def keyboard(data: str, dictionaries: list[Dictionary]):
        builder = InlineKeyboardBuilder()
        buttons = [
            InlineKeyboardButton(
                text=dictionary.name,
                callback_data=DictionariesKeyboard(data=data, id=dictionary.id).pack(),
            )
            for dictionary in dictionaries
        ]
        builder.add(*buttons)
        builder.adjust(2)
        builder.row(
            InlineKeyboardButton(
                text=str(Text.VIEW_BUTTON), web_app=WebAppInfo(url=f"{settings.FRONTEND_URL}/dictionaries")
            )
        )
        return builder.as_markup()
