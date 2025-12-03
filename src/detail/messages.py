from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.api import Vendor
from src.messagesutils import get_date_relname, get_lesson_description, find_by_date


def get_date_lesson_detail(dt: date,
                           lesson_num: int,
                           prev_msg: str,
                           vendor: Vendor) -> dict:
    lesson = find_by_date(dt, vendor).lessons[lesson_num]

    result = f"<b>📚 {lesson.num}-й урок — "
    name = get_date_relname(lesson.date, False)
    if name != "":
        result += f"{name}, "
    result += lesson.date.strftime("%d %B %Y").lower() + "</b>\n\n"
    result += get_lesson_description(lesson, end_time=True, room=True, topic=True, teacher=True)

    return_button = None
    if prev_msg == "homework":
        return_button = InlineKeyboardButton(
            text="Назад",
            callback_data=f"homeworks_list_{lesson.date.isoformat()}"
        )
    elif prev_msg == "week":
        return_button = InlineKeyboardButton(
            text="Назад",
            callback_data=f"week_timetable_{lesson.date.isoformat()}"
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [return_button]
    ])

    return {
        "text": result,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }
