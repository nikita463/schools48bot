from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL)
Session = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
