from datetime import date, timedelta

from src.api import Vendor, Day
from src.api.typings import Homework, Lesson
from src.updates import weeks_diary


def find_by_date(target_date: date, vendor: Vendor) -> Day | None:
    for day in weeks_diary[vendor.tg_id][vendor.student_name].days:
        if day.date == target_date:
            return day
    return None


def get_lesson_emoji(name: str) -> str:
    """Возвращает эмодзи, соответствующее названию предмета"""

    if name == "Иностранный язык (английский)":
        return "🇬🇧"
    elif name == "Химия":
        return "🧪"
    elif name == "Литература":
        return "📖"
    elif name == "Геометрия":
        return "📐"
    elif name == "История":
        return "📜"
    elif name == "Физика":
        return "🔬"
    elif name == "Обществознание":
        return "⚖️"
    elif name == "Алгебра и начала математического анализа":
        return "📘"
    elif name == "Биология":
        return "🧬"
    elif name == "География":
        return "🌍"
    elif name == "Русский язык":
        return "✍️"
    elif name == "Вероятность и статистика":
        return "📊"
    elif name == "Индивидуальный проект":
        return "📝"
    elif name == "Информатика" or name == "Информационная безопасность":
        return "💻"
    elif name == "Классный час":
        return "👥"
    elif name == "Разговоры о важном":
        return "💬"
    elif name == "Россия - мои горизонты":
        return "🌅"
    elif name == "Физическая культура":
        return "⚽"
    elif name == "Основы безопасности и защиты Родины":
        return "🇷🇺"
    else:
        print("Unexpected subject:", name)
        return ""


def get_date_relname(dt: date, upper: bool) -> str:
    """Возвращает относительное имя дня"""

    relname = ""
    if dt == date.today() - timedelta(days=2):
        relname = "Позавчера"
    elif dt == date.today() - timedelta(days=1):
        relname = "Вчера"
    elif dt == date.today():
        relname = "Сегодня"
    elif dt == date.today() + timedelta(days=1):
        relname = "Завтра"
    elif dt == date.today() + timedelta(days=2):
        relname = "Послезавтра"

    return relname if upper else relname.lower()


def get_date_title(dt: date) -> str:
    """Возвращает в виде строки заголовок с датой. Пример:

    📅 <b>Сегодня — Вторник, 25 ноября 2025</b>"""

    name = get_date_relname(dt, True)
    formatted_date = dt.strftime("%A, %d %B %Y")
    formatted_date = formatted_date[0].upper() + formatted_date[1:]
    if name != "":
        return "📅 <b>" + name + " — " + formatted_date + "</b>"
    return "📅 <b>" + formatted_date + "</b>"


def get_homework_description(homework: Homework) -> str:
    """Возвращает описание одной домашней работы"""
    result = f"<i>{homework.text}</i>"
    for file in homework.files:
        result += f'\n  <a href="{file.link}">🖇 {file.filename}</a>'
    result += "\n"
    return result


def get_lesson_description(lesson: Lesson,
                           end_time: bool = False,
                           room: bool = False,
                           topic: bool = False,
                           teacher: bool = False) -> str:
    """Возвращает описание одного урока"""

    result = ""
    lesson_emoji = get_lesson_emoji(lesson.name)
    if lesson.start:
        result += f"{lesson.start:%H:%M}"
        if end_time and lesson.end:
            result += f" - {lesson.end:%H:%M}"
        result += " — "
    result += f"{lesson_emoji} <b>{lesson.name}</b>"

    if room:
        result += f"\n\n<b>Кабинет:</b> {lesson.room}\n"
    else:
        result += f" — <b>кабинет {lesson.room}</b>\n"

    if teacher: result += f"<b>Учитель:</b> {lesson.teacher}\n"

    if topic and len(lesson.topic) > 0: result += f"<b>Тема:</b> {lesson.topic}\n"

    if room or topic or teacher:
        result += "\n"

    if len(lesson.homeworks) > 0:
        result += "<blockquote>📝 <i>ДЗ:</i>"
        if len(lesson.homeworks) == 1:
            result += " " + get_homework_description(lesson.homeworks[0])
        else:
            result += "\n"
            for homework in lesson.homeworks:
                result += "• " + get_homework_description(homework)
        result += "</blockquote>"
    return result
