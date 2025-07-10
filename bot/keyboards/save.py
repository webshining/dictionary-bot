from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SaveKeyboard(CallbackData, prefix="save"):
    id: int

    @staticmethod
    def keyboard(id: int):
        builder = InlineKeyboardBuilder()

        builder.button(text="Save", callback_data=SaveKeyboard(id=id).pack())

        return builder.as_markup()
