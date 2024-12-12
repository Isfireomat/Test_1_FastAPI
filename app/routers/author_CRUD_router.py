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
                   AuthorSchema, BookSchema, BorrowSchema, \
                   BorrowCreateSchema

author_router = APIRouter()

@author_router.post('/authors', routing_model=AuthorSchema)
async def author_create(
                        response: Response, 
                        author: AuthorSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Создание автора (POST /authors).    
    """
    return author


@author_router.get('/authors', routing_model=List[AuthorSchema])
async def author_read_list(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение списка авторов (GET /authors).
    """
    return []

@author_router.get('/authors/{id}', routing_model=AuthorSchema)
async def author_read(
                        response: Response, 
                        id: int,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение информации об авторе по id (GET /authors/{id}).
    """
    return id


@author_router.put('/authors/{id}', routing_model=AuthorSchema)
async def author_update(
                        response: Response, 
                        author: AuthorSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Обновление информации об авторе (PUT /authors/{id}).
    """
    return author


@author_router.delete('/authors/{id}', routing_model=Dict[str:str])
async def author_delete(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Удаление автора (DELETE /authors/{id}).
    """
    return {'Message':'delete successful'}