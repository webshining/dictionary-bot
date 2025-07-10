from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DictionaryKeyboard(CallbackData, prefix="dictionary"):
    id: int
    action: str

    @staticmethod
    def keyboard(id: int):
        builder = InlineKeyboardBuilder()
        buttons = [
            InlineKeyboardButton(
                text="View",
                web_app=WebAppInfo(url=f"https://calm-composed-gobbler.ngrok-free.app/webapp/dictionary/{id}/init"),
            ),
        ]
        builder.add(*buttons)
        return builder.as_markup()
