import os
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.data_base import get_session
from app.models import Base
from app.main import app

from typing import AsyncGenerator

DATABASE_URL: str = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres"
DATABASE_URL_TEST = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/test_db"

async def create_test_database():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("COMMIT")) 
        await conn.execute(text("CREATE DATABASE test_db"))
    await engine.dispose()

async def drop_test_database():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("COMMIT")) 
        await conn.execute(text("DROP DATABASE IF EXISTS test_db WITH (FORCE)"))
    await engine.dispose()

async def create_tables():
    engine = create_async_engine(DATABASE_URL_TEST)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

async def drop_tables():
    engine = create_async_engine(DATABASE_URL_TEST)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function",  autouse=True)
async def test_database():
    try:
        await create_test_database()
    except ProgrammingError:
        print("Тестовая БД уже существует.")
    await create_tables()
    yield 
    await drop_test_database()


@pytest_asyncio.fixture
async def app_with_test_db():
    engine_test = create_async_engine(DATABASE_URL_TEST)
    session_local_test = async_sessionmaker(bind=engine_test, class_=AsyncSession)    
    async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_local_test() as session:
            try:
                yield session
                await session.commit()
            except:
                await session.rollback()
                raise
            finally:
                await session.close()
    app.dependency_overrides[get_session] = get_test_session
    yield app
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def async_client(app_with_test_db):
    transport = ASGITransport(app=app_with_test_db)
    async with AsyncClient(
        transport=transport,
        base_url=F"http://localhost:{os.getenv('PORT')}") as client:
        yield client

@pytest_asyncio.fixture
async def author():
    return {
        "name": 'Ruslan',
        "surname": 'Mazura',
        "birthday": '2000-01-01'
    }

@pytest_asyncio.fixture
async def book():
    return {
        "title": 'Metrto 2036',
        "description": 'without description',
        "author_id": 1,
        "count_available": 2
    }

@pytest_asyncio.fixture
async def borrow():
    return {
        "book_id": 1,
        "reader_name": 'Isfireomat',
        "date_borrow": '2020-12-21'
    }

@pytest_asyncio.fixture
async def return_date():
    return {
         "return_date": "2024-12-14"
    }

@pytest_asyncio.fixture
async def author_create(async_client: AsyncClient, author):
    response = await async_client.post("/api/authors", json=author)
    return response.json()

@pytest_asyncio.fixture
async def book_create(async_client: AsyncClient, author_create, book):
    response = await async_client.post("/api/books", json=book)
    return response.json()