from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.api.typings import Day, Vendor
from src.messagesutils import get_date_title, get_lesson_description, find_by_date


def gen_diary(day: Day) -> str:
    result = get_date_title(day.date) + "\n"
    for i, lesson in enumerate(day.lessons):
        result += f"\n{i + 1}) " + get_lesson_description(lesson)
    return result


def gen_date_diary(dt: date, vendor: Vendor) -> str:
    day = find_by_date(dt, vendor)
    if day is None:
        result = get_date_title(dt) + "\n\n"
        result += "На этот день уроков нет\n"
        return result
    return gen_diary(day)


def get_week_diary(dt: date, vendor: Vendor) -> dict:
    monday = dt - timedelta(days=dt.weekday())
    if dt.weekday() >= 5:
        monday += timedelta(weeks=1)
        dt = monday

    date_buttons = []
    for i in range(0, 5):
        curr_date = monday + timedelta(days=i)
        if i == dt.weekday():
            text = "🟢 " + curr_date.strftime("%d %b")
        else:
            text = curr_date.strftime("%d %b")
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"week_timetable_" + curr_date.isoformat()
        )
        date_buttons.append(button)

    current_monday = date.today() - timedelta(days=date.today().weekday())
    if current_monday == monday:
        change_week_button = InlineKeyboardButton(
            text="Следующая неделя",
            callback_data=f"week_timetable_" + (monday + timedelta(weeks=1)).isoformat()
        )
    else:
        next_week_date = date.today()
        if date.today().weekday() >= 5:
            next_week_date = current_monday + timedelta(days=4)
        change_week_button = InlineKeyboardButton(
            text="Текущая неделя",
            callback_data=f"week_timetable_" + next_week_date.isoformat()
        )

    lessons_button_tip = InlineKeyboardButton(text="Подробности уроков", callback_data="tip_lesson_detail")

    lessons_buttons = []
    day = find_by_date(dt, vendor)
    if day:
        for lesson in day.lessons:
            lessons_buttons.append(InlineKeyboardButton(
                text=lesson.num,
                callback_data=f"lesson_detail_week_{int(lesson.num) - 1}_{dt.isoformat()}"
            ))

    text = gen_date_diary(dt, vendor)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [lessons_button_tip],
        lessons_buttons,
        date_buttons[:2],
        date_buttons[2:],
        [change_week_button]
    ])

    return {
        "text": text,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }


def get_today_diary(vendor: Vendor) -> dict:
    return {
        "text": gen_date_diary(date.today(), vendor),
        "parse_mode": "HTML"
    }


def get_tomorrow_diary(vendor: Vendor) -> dict:
    return {
        "text": gen_date_diary(date.today() + timedelta(days=1), vendor),
        "parse_mode": "HTML"
    }
