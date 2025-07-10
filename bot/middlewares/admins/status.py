from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.types import CallbackQuery, InlineQuery, Message

from users.models import User


async def status_middleware(event: TelegramEventObserver):
    @event.middleware()
    async def process(handler, event: Message | CallbackQuery | InlineQuery, data):
        user: User = data["user"]
        if not user.is_superuser:
            return
        return await handler(event, data)
