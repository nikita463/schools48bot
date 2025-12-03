from sqlalchemy import select

from src.api import api_get_vendor, Vendor
from src.database import Session
from .models import UserOrm
from .schemas import User


async def get_user(tg_id: int) -> User | None:
    async with Session() as session:
        stmt = (
            select(UserOrm)
            .where(UserOrm.tg_id == tg_id)
        )

        user = await session.scalar(stmt)

        return User.model_validate(user, from_attributes=True) if user else None


async def get_vendor(tg_id: int) -> Vendor | None:
    user = await get_user(tg_id)
    if user is None: return None

    vendor = await api_get_vendor(user.v_token)
    if vendor is None: return None
    vendor.student_name = user.student_name
    vendor.tg_id = tg_id

    return vendor
