from datetime import date

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.homework.messages import get_week_homeworks
from src.user import get_vendor
from src.utils import check_user

router = Router()


@router.message(Command("homework"))
async def handle_week_homeworks_list(message: Message):
    if check_user(message.from_user): return
    vendor = await get_vendor(message.from_user.id)

    await message.answer(**get_week_homeworks(date.today(), vendor))


@router.callback_query(F.data.startswith("homeworks_list"))
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user): return
    vendor = await get_vendor(callback.from_user.id)

    callback_data = callback.data.removeprefix("homeworks_list_")
    next_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**get_week_homeworks(next_date, vendor))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)
