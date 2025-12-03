import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from src.updates import run_update_diary
from src.utils import check_user
from src.database import create_all
from src.config import settings

from src.diary import diary_router
from src.homework import homework_router
from src.detail import detail_router

bot = Bot(settings.bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def handle_start(message: Message):
    if check_user(message.from_user): return

    text = ("/today - Расписание на сегодня\n"
            "/tomorrow - Расписание на завтра\n"
            "/week - расписание на неделю")
    await message.answer(text)


async def main():
    await create_all()

    dp.include_router(diary_router)
    dp.include_router(homework_router)
    dp.include_router(detail_router)

    await run_update_diary(1758224988)
    await dp.start_polling(bot)

asyncio.run(main())
