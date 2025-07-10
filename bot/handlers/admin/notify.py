import asyncio

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _

from bot.keyboards import ApplyKeyboard
from bot.states import NotifyState
from users.models import User
from utils import logger

from ..routes import admin_router as router


@router.message(Command("notify"))
async def _notify(message: Message, state: FSMContext):
    await message.answer(_("Enter message text:"))
    await state.set_state(NotifyState.text)


@router.message(NotifyState.text)
async def _notify_to_message(message: Message, state: FSMContext):
    await message.copy_to(chat_id=message.chat.id, reply_markup=ApplyKeyboard.keyboard("notify"))
    await message.delete()
    await state.set_state(None)


@router.callback_query(ApplyKeyboard.filter(F.data == "notify"))
async def _notify_to(call: CallbackQuery):
    users = await sync_to_async(list)(User.objects.all())
    for u in users:
        try:
            await call.message.copy_to(chat_id=u.telegram_id, reply_markup=None)
        except Exception as e:
            logger.error(e)
            logger.error(f"message for {u.id} was not sent")
        await asyncio.sleep(0.5)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
