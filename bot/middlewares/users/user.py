from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.types import CallbackQuery, InlineQuery, Message
from django.utils.translation import override

from users.models import User


async def user_middleware(
    event: TelegramEventObserver,
):
    @event.middleware()
    async def process(
        handler,
        event: Message | CallbackQuery | InlineQuery,
        data,
    ):
        await process_user(event.from_user, data)
        with override(data["user"].language_code):
            await handler(event, data)

    async def process_user(from_user, data):
        user, created = await User.objects.aupdate_or_create(
            telegram_id=from_user.id,
            defaults={
                "telegram_username": from_user.username,
                "first_name": from_user.first_name,
                "last_name": from_user.last_name,
            },
        )
        if created and user.language_code != from_user.language_code:
            user.language_code = from_user.language_code
            await user.asave(update_fields=["language_code"])
        data["user"] = user
