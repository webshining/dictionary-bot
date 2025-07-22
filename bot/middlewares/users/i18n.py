from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.types import Message, CallbackQuery, InlineQuery
from django.utils.translation import override

from users.models import User


async def i18n_middleware(event: TelegramEventObserver):
    @event.outer_middleware()
    async def process(handler, event: Message | CallbackQuery | InlineQuery, data):
        user: User = data["user"]
        with override(user.language_code):
            await handler(event, data)
