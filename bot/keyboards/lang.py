from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings


class LangKeyboard(CallbackData, prefix="lang"):
    lang: str

    @staticmethod
    def keyboard():
        builder = InlineKeyboardBuilder()

        for code, lang in settings.LANGUAGES:
            builder.button(
                text=lang,
                callback_data=LangKeyboard(lang=code).pack(),
            )
        builder.adjust(3)

        return builder.as_markup()
