from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("sqlite+aiosqlite:///./app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db
