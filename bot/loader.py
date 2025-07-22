from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n
from django.conf import settings

bot = Bot(
    settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
    ),
)

i18n = I18n(path=settings.BASE_DIR.joinpath("locale"), domain="django")
_ = i18n.gettext
