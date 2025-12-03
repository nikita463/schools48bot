from datetime import date

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.utils import check_user
from src.user import get_vendor
from .messages import get_today_diary, get_tomorrow_diary, get_week_diary

router = Router()


@router.message(Command("today"))
async def handle_today_timetable(message: Message):
    if check_user(message.from_user): return
    vendor = await get_vendor(message.from_user.id)

    await message.answer(**get_today_diary(vendor))


@router.message(Command("tomorrow"))
async def handle_tomorrow_timetable(message: Message):
    if check_user(message.from_user): return
    vendor = await get_vendor(message.from_user.id)

    await message.answer(**get_tomorrow_diary(vendor))


@router.message(Command("week"))
async def handle_week_timetable(message: Message):
    if check_user(message.from_user): return
    vendor = await get_vendor(message.from_user.id)

    await message.answer(**get_week_diary(date.today(), vendor))


@router.callback_query(F.data.startswith("week_timetable"))
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user): return
    vendor = await get_vendor(callback.from_user.id)

    callback_data = callback.data.removeprefix("week_timetable_")
    next_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**get_week_diary(next_date, vendor))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)
