from aiogram.filters import Filter
from aiogram.types import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from loader import _, i18n


class BaseInlineKeyboard:
    @classmethod
    def keyboard(cls, *args, **kwargs) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(*cls.buttons(*args, **kwargs))
        builder.adjust(kwargs.get("adjust", 2))
        return builder.as_markup()


class BaseReplyKeyboard(Filter):
    def __init__(self, word: str):
        self.word = word

    async def __call__(self, message: Message):
        return message.text in [_(self.word, locale=lang) for lang in i18n.available_locales]

    @classmethod
    def keyboard(cls, *args, **kwargs) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.add(*cls.buttons(*args, **kwargs))
        builder.adjust(kwargs.get("adjust", 2))
        return builder.as_markup(resize_keyboard=True)
