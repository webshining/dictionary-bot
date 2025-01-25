from aiogram.filters.callback_data import CallbackData
from aiogram.types import WebAppInfo

from .base import BaseInlineKeyboard


class CardMarkupClass(BaseInlineKeyboard):
    def keyboard(self):
        builder = self.builder()

        builder.button(text="Card", web_app=WebAppInfo(url="https://calm-composed-gobbler.ngrok-free.app/cards"))

        return builder.as_markup()

    class Callback(CallbackData, prefix="card"):
        pass


CardMarkup = CardMarkupClass()
