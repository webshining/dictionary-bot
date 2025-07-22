from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.text import Text


class SaveKeyboard(CallbackData, prefix="save"):
    id: int

    @staticmethod
    def keyboard(id: int):
        builder = InlineKeyboardBuilder()

        builder.button(text=str(Text.SAVE_BUTTON), callback_data=SaveKeyboard(id=id).pack())

        return builder.as_markup()
