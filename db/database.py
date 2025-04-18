from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

DATABASE_URL = "sqlite+aiosqlite:///./db/cheese.db"


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


metadata = MetaData()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
