from typing import Generator
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=False,
    poolclass=NullPool,
)

session_maker = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    with session_maker() as db:
        try:
            yield db
        except Exception as e:
            db.rollback()
            raise e