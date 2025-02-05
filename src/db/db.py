from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config.config import (DB_USER, DB_PASS,
                           DB_HOST, DB_PORT, DB_NAME)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
