from typing import Dict, Optional, Union, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from app.data_base import get_session, get_book_by_id, create_borrow, \
                      get_borrow_by_id, update_return_date_borrow, \
                      update_book_count_available_by_id
from app.models import Author, Book, Borrow, \
                   BookSchema, BookSchema, BorrowSchema, \
                   BorrowCreateSchema

book_router = APIRouter()

# 
# 
# 
# 
# 

@book_router.post('/books', routing_model=BookSchema)
async def author_create(
                        response: Response, 
                        book: BookSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Добавление книги (POST /books).   
    """
    return book


@book_router.get('/books', routing_model=List[BookSchema])
async def author_read_list(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение списка книг (GET /books).
    """
    return []

@book_router.get('/books/{id}', routing_model=BookSchema)
async def author_read(
                        response: Response, 
                        id: int,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение информации о книге по id (GET /books/{id}).
    """
    return id


@book_router.put('/books/{id}', routing_model=BookSchema)
async def author_update(
                        response: Response, 
                        book: BookSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Обновление информации о книге (PUT /books/{id}).
    """
    return book


@book_router.delete('/books/{id}', routing_model=Dict[str:str])
async def author_delete(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Удаление книги (DELETE /books/{id}).
    """
    return {'Message':'delete successful'}