from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.api import Lesson, Vendor
from src.homework.utils import get_homeworks_list
from src.messagesutils import get_date_relname, get_lesson_description


def get_week_homeworks(dt: date,
                       vendor: Vendor) -> dict:
    monday = dt - timedelta(days=dt.weekday())
    if dt.weekday() >= 5:
        monday += timedelta(weeks=1)
        dt = monday

    date_buttons = []
    for i in range(0, 5):
        if i == dt.weekday():
            text = "🟢 " + (monday + timedelta(days=i)).strftime("%d %b")
        else:
            text = (monday + timedelta(days=i)).strftime("%d %b")
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"homeworks_list_" + (monday + timedelta(days=i)).isoformat()
        )
        date_buttons.append(button)

    current_monday = date.today() - timedelta(days=date.today().weekday())
    if current_monday == monday:
        change_week_button = InlineKeyboardButton(
            text="Следующая неделя",
            callback_data=f"homeworks_list_" + (monday + timedelta(weeks=1)).isoformat()
        )
    else:
        next_week_date = date.today()
        if date.today().weekday() >= 5:
            next_week_date = current_monday + timedelta(days=4)
        change_week_button = InlineKeyboardButton(
            text="Текущая неделя",
            callback_data=f"homeworks_list_" + next_week_date.isoformat()
        )

    lessons_button_tip = InlineKeyboardButton(text="Подробности уроков", callback_data="tip_lesson_detail")

    homeworks_list = get_homeworks_list(vendor)
    lessons_buttons = []
    for lesson in homeworks_list:
        if lesson.date == dt:
            lessons_buttons.append(InlineKeyboardButton(
                text=lesson.num,
                callback_data=f"lesson_detail_homework_{int(lesson.num) - 1}_{dt.isoformat()}"
            ))

    text = get_date_homeworks(dt, vendor)
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


def get_date_homeworks(
        dt: date,
        vendor: Vendor) -> str:
    """Возвращает в виде строки список уроков в определенную дату, на которые назначены домашние работы"""

    result = "📝 <b>Домашние задания на "
    name = get_date_relname(dt, False)
    if name != "":
        result += name + ", "
    result += dt.strftime("%d %B %Y").lower() + "</b>\n\n"

    homeworks_list = get_homeworks_list(vendor)
    date_homework_lessons: list[Lesson] = []
    for lesson in homeworks_list:
        if lesson.date == dt:
            date_homework_lessons.append(lesson)

    for lesson in sorted(date_homework_lessons, key=lambda x: (x.date, x.start)):
        result += f"{lesson.num}) " + get_lesson_description(lesson) + "\n"

    return result
