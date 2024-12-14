from typing import Dict
import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_author_router(async_client: AsyncClient, author: Dict):
    response = await async_client.post("/api/authors", json=author)
    assert response.status_code == 200
    first_response_dict = response.json()
    id: int = first_response_dict['id']
    
    response = await async_client.get(f"/api/authors/{id}")
    assert response.status_code == 200
    assert first_response_dict == response.json()
    
    response = await async_client.get("/api/authors")
    assert response.status_code == 200
    assert first_response_dict in response.json()
    
    author['name'] = 'Name'
    author['surname'] = 'Surname'
    response = await async_client.put(f"/api/authors/{id}", json=author)
    assert response.status_code == 200
    assert first_response_dict != response.json()
    
    response = await async_client.delete(f"/api/authors/{id}")
    assert response.status_code == 200
    response = await async_client.delete(f"/api/authors/{id}")
    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_book_router(async_client: AsyncClient, book: Dict, author_create):
    response = await async_client.post("/api/books", json=book)
    assert response.status_code == 200
    first_response_dict = response.json()
    id: int = first_response_dict['id']
    
    response = await async_client.get(f"/api/books/{id}")
    assert response.status_code == 200
    assert first_response_dict == response.json()
    
    response = await async_client.get("/api/books")
    assert response.status_code == 200
    assert first_response_dict in response.json()
    
    book['title'] = 'Name'
    response = await async_client.put(f"/api/books/{id}", json=book)
    assert response.status_code == 200
    assert first_response_dict != response.json()
    
    response = await async_client.delete(f"/api/books/{id}")
    assert response.status_code == 200
    response = await async_client.delete(f"/api/books/{id}")
    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_borrow_router(async_client: AsyncClient, borrow: Dict, book_create, return_date):
    first_book_count_available = book_create['count_available']
    response = await async_client.post("/api/borrows", json=borrow)
    assert response.status_code == 200
    first_response_dict = response.json()
    book_id: int = first_response_dict['book_id'] 
    id: int = first_response_dict['id']
    
    response = await async_client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    second_book_count_available = response.json()['count_available']
    assert first_book_count_available > second_book_count_available
    
    response = await async_client.get(f"/api/borrows/{id}")
    assert response.status_code == 200
    assert first_response_dict == response.json()
    
    response = await async_client.get("/api/borrows")
    assert response.status_code == 200
    assert first_response_dict in response.json()
    
    borrow['reader_name'] = 'Name'
    response = await async_client.put(f"/api/borrows/{id}", json=borrow)
    assert response.status_code == 200
    assert first_response_dict != response.json()
    
    response = await async_client.patch(f"/api/borrows/{book_id}/return", json=return_date)
    assert response.status_code == 200
    response = await async_client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    third_book_count_available = response.json()['count_available']
    assert first_book_count_available == third_book_count_available
    
    response = await async_client.delete(f"/api/borrows/{id}")
    assert response.status_code == 200
    response = await async_client.delete(f"/api/borrows/{id}")
    assert response.status_code == 404