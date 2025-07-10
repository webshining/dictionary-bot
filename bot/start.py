from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utils import logger
from .commands import set_default_commands
from .handlers import setup_routes
from .loader import bot
from .middlewares import setup_middlewares

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_startup():
    await set_default_commands()
    logger.info(f"Bot started as {(await bot.get_me()).username} (ID: {bot.id})")


async def on_shutdown():
    logger.info("Bot is shutting down")


async def start():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await setup_middlewares(dp)
    await setup_routes(dp)
    await dp.start_polling(bot)
