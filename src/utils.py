import asyncio
from datetime import datetime
from traceback import print_exc

from aiogram.types import User as TgUser

from src.config import settings


def get_message_args(text: str) -> set:
    args = text.split()
    return {*args[1:]} if len(args) > 0 else {}


def check_user(user: TgUser) -> bool:
    if user.id not in settings.white_list_users:
        print(f"Request from unknown user, id: {user.id}, username: {user.username}")
    return False


def run_at(run_time: datetime):
    def deco(func):
        async def wrapper(*args, **kwargs):
            now = datetime.now()
            delay = (run_time - now).total_seconds()
            if delay > 0:
                await asyncio.sleep(delay)
            try:
                return await func(*args, **kwargs)
            except Exception as exp:
                print("[ERROR] run_every()" + str(exp))
                print_exc()
                return None
        return wrapper
    return deco


def run_every(interval: int):
    def deco(func):
        async def wrapper(*args, **kwargs):
            while True:
                try:
                    await func(*args, **kwargs)
                except Exception as exp:
                    print("[ERROR] run_every() " + str(exp))
                    print_exc()
                await asyncio.sleep(interval)
        return wrapper
    return deco
