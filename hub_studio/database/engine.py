import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from hub_studio.database.models import Base

# DB_LITE=sqlite+aiosqlite:///bot_pizza/database/my_base.db
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name

engine = create_async_engine(os.getenv("DB_URL"), echo=True)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Стандартная функция для создания всех таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
