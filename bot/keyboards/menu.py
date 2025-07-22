from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.text import Text


def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=str(Text.DICTIONARIES_BUTTON)), KeyboardButton(text=str(Text.CARDS_BUTTON)))
    builder.row(KeyboardButton(text=str(Text.LANGUAGE_BUTTON)))

    return builder.as_markup(resize_keyboard=True)
