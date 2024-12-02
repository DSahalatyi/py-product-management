import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


ASYNC_DB_URL = (f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
                f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
                f"{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
#
# SYNC_DB_URL = (f"postgresql://{os.getenv('POSTGRES_USER')}:"
#                f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
#                f"{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"


engine_async = create_async_engine(ASYNC_DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
