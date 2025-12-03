from datetime import date

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from src.detail.messages import get_date_lesson_detail
from src.user import get_vendor
from src.utils import check_user

router = Router()


@router.callback_query(F.data == "tip_lesson_detail")
async def callback_lesson_detail_tip(callback: CallbackQuery):
    if check_user(callback.from_user): return

    await callback.answer(
        text="Нажмите на кнопку с номером урока, чтобы получить его подробное описание",
        show_alert=True
    )


@router.callback_query(F.data.startswith("lesson_detail"))
async def callback_lesson_detail(callback: CallbackQuery):
    if check_user(callback.from_user): return
    vendor = await get_vendor(callback.from_user.id)

    callback_data = callback.data.removeprefix("lesson_detail_")
    prev_msg = callback_data[:callback_data.find("_")]

    callback_data = callback_data[callback_data.find("_") + 1:]
    lesson_num = int(callback_data[:callback_data.find("_")])

    callback_data = callback_data[callback_data.find("_") + 1:]
    lesson_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**get_date_lesson_detail(lesson_date, lesson_num, prev_msg, vendor))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)
