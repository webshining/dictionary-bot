from aiogram.types import KeyboardButton, WebAppInfo

from loader import _
from .base import BaseReplyKeyboard


class MenuKeyboardClass(BaseReplyKeyboard):
    def keyboard(self):
        builder = self.builder()

        buttons = [
            KeyboardButton(text=_("Open dictionary"),
                           web_app=WebAppInfo(url="https://calm-composed-gobbler.ngrok-free.app/cards"))]
        builder.add(*buttons)

        return builder.as_markup(resize_keyboard=True)


MenuKeyboard = MenuKeyboardClass()
