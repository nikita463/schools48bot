import asyncio
from locale import setlocale, LC_TIME
from datetime import date, timedelta

from src.api import get_diary, Student
from src.config import settings
from src.user import get_vendor
from src.utils import run_every

setlocale(LC_TIME, "ru_RU.UTF-8")

weeks_diary: dict[int, dict[str, Student]] = dict()


@run_every(settings.update_interval)
async def update(tg_id: int):
    global weeks_diary

    vendor = await get_vendor(tg_id)
    if vendor is None:
        print("[ERROR] update_diary(): vendor not received")
        return

    today = date.today()
    weekday = today.weekday()

    start_of_current_week = today - timedelta(days=weekday)
    end_of_current_week = start_of_current_week + timedelta(days=6)
    start_of_next_week = start_of_current_week + timedelta(days=7)
    end_of_next_week = start_of_next_week + timedelta(days=6)

    current_week_diary = await get_diary(start_of_current_week, end_of_current_week, vendor)
    next_week_diary = await get_diary(start_of_next_week, end_of_next_week, vendor)

    if current_week_diary is None:
        print("[ERROR] update_diary(): current_week_diary not received")
        return
    if next_week_diary is None:
        print("[ERROR] update_diary(): next_week_diary not received")
        return

    weeks_diary.clear()
    weeks_diary.update({tg_id: current_week_diary})

    for key, new_student in next_week_diary.items():
        if key in weeks_diary[tg_id]:
            existing = weeks_diary[tg_id][key]
            existing.days.extend(new_student.days)
        else:
            weeks_diary[tg_id][key] = new_student

    print("diary updated")


async def run_update_diary(tg_id: int):
    asyncio.create_task(update(tg_id))
