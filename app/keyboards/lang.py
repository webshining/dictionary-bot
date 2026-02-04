from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class LangKeyboard(CallbackData, prefix="lang"):
    lang: int | str
    data: str

    @staticmethod
    def keyboard(data: str, languages: list[list], selected: list):
        builder = InlineKeyboardBuilder()

        for key, lang in languages:
            builder.button(
                text=f'{lang}{"*" if key in selected else ""}',
                callback_data=LangKeyboard(data=data, lang=key).pack(),
            )
        builder.adjust(3)

        return builder.as_markup()
