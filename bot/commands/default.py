from aiogram.types import BotCommand, BotCommandScopeDefault
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import override

from bot.loader import bot


def get_default_commands(lang: str = "en"):
    with override(lang):
        commands = [
            BotCommand(command="/start", description=_("start chat")),
            BotCommand(command="/lang", description=_("change language")),
        ]

    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in settings.LANGUAGES:
        await bot.set_my_commands(get_default_commands(lang[0]), scope=BotCommandScopeDefault(), language_code=lang[0])
