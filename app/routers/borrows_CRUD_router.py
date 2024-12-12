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
                   BorrowSchema, BookSchema, BorrowSchema, \
                   BorrowCreateSchema

barrow_router = APIRouter()

# Создание записи о выдаче книги (POST /borrows).
# Получение списка всех выдач (GET /borrows).
# Получение информации о выдаче по id (GET /borrows/{id}).
# Завершение выдачи (PATCH /borrows/{id}/return) с указанием даты возврата.

@barrow_router.post('/borrow', routing_model=BorrowSchema)
async def author_create(
                        response: Response, 
                        borrow: BorrowSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Создание автора (POST /borrow).    
    """
    return borrow


@barrow_router.get('/borrow', routing_model=List[BorrowSchema])
async def author_read_list(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение списка авторов (GET /borrow).
    """
    return []

@barrow_router.get('/borrow/{id}', routing_model=BorrowSchema)
async def author_read(
                        response: Response, 
                        id: int,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Получение информации об авторе по id (GET /borrow/{id}).
    """
    return id


@barrow_router.put('/borrow/{id}', routing_model=BorrowSchema)
async def author_update(
                        response: Response, 
                        borrow: BorrowSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Обновление информации об авторе (PUT /borrow/{id}).
    """
    return borrow


@barrow_router.delete('/borrow/{id}', routing_model=Dict[str:str])
async def author_delete(
                        response: Response, 
                        session: AsyncSession = Depends(get_session)
                    ):
    """
    Удаление автора (DELETE /borrow/{id}).
    """
    return {'Message':'delete successful'}