from os import environ
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from app.models import Base

DATABASE_URL: str = f"postgresql+asyncpg://{environ.get('DB_USER')}:{environ.get('DB_PASS')}@{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_NAME')}"

engine: Engine = create_async_engine(DATABASE_URL)
async_session_local = sessionmaker(bind=engine,class_=AsyncSession)

async def create_start_table() -> None:
    """
    При старте создаёт таблицы
    """
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all(bind=engine))

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Возвращает сессию psql и при ошибке в работе с сессией
    откатывает изменения
    
    session - сессия подключения к БД
    возвращаем session
    """
    async with async_session_local() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()