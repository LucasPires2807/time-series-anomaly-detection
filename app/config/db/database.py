from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=2,
    max_overflow=0,
    pool_timeout=120,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session_maker() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e