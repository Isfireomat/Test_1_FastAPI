import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest_asyncio.fixture
async def author():
    return {
        "name": 'Ruslan',
        "surname": 'Mazura',
        "birthday": '01-01-2000'
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
async def barrow():
    return {
        "book_id": 1,
        "reader_name": 'Isfireomat',
        "date_borrow": '25-01-2020'
    }
    

@pytest.mark.asyncio
async def test_author_routers(async_client: AsyncClient, user_data):
    response = await async_client.post("/api/registration/", json=user_data)
    assert response.status_code == 200
