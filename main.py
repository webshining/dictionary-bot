import asyncio

from aiogram.methods import DeleteWebhook

from app import set_default_commands, setup_middlewares, setup_routes
from loader import bot, dp
from utils import logger


async def on_startup() -> None:
    await set_default_commands()
    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.info("Bot stopped!")


async def main() -> None:
    await setup_middlewares(dp)
    await setup_routes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
