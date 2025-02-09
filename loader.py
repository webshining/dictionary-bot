from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from redis.asyncio import ConnectionPool, Redis

from data.config import I18N_DOMAIN, I18N_PATH, RD_URI, TELEGRAM_BOT_TOKEN

bot = Bot(
    TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
)

redis_pool = ConnectionPool.from_url(RD_URI)
redis_session = Redis.from_pool(redis_pool)
redis_bot = Redis.from_pool(redis_pool)
storage = RedisStorage(redis_bot)
dp = Dispatcher(storage=storage)

i18n = I18n(path=I18N_PATH, domain=I18N_DOMAIN)
_ = i18n.gettext
