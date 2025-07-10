from aiogram import Dispatcher

from .admin import router as admin_router
from .user import router as user_router


async def setup_routes(dp: Dispatcher):
    dp.include_routers(user_router, admin_router)


__all__ = ["setup_routes"]
