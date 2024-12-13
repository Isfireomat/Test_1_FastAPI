from typing import Dict, Optional, Union, List, Type, TypeVar
from pydantic import BaseModel
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.data_base import get_session, \
                       update_return_date_borrow, \
                      update_book_count_available_by_id, CRUD
from app.models import Author, Book, Borrow, \
                   AuthorSchema, BookSchema, BorrowSchema

def http_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            object = await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f'{e}'
            )
        if not object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Object not found'
                )
        return object
    return wrapper

T = TypeVar("T", bound=BaseModel)    

def create_CRUD_router(
        model, 
        schema: Type[T],
        api: str,
        session: AsyncSession
    ):
    
    crud = CRUD(model=model)
    router = APIRouter()
    
    class Id:
        id: int      
    
    class WithId(schema,Id):
        class Config:
            from_attributes = True
            
    @router.post(f'{api}', response_model=WithId)
    async def create(
                    response: Response, 
                    object: schema,
                    session: AsyncSession = Depends(session)
                ):
        """
        Создание объекта в БД и получение его.     
        """
        @http_handler
        async def handler():
            return await crud.create(
                    session=session,
                    object=object 
                )
        return await handler()

    @router.get(f'{api}/{{id}}', response_model=WithId)
    async def read(
                    response: Response, 
                    id: int,
                    session: AsyncSession = Depends(session)
                ):
        """
        Получение объекта.
        """
        @http_handler
        async def handler():
            return await crud.read(
                    session=session,
                    id=id
                )
        return await handler()

    @router.get(f'{api}', response_model=List[WithId])
    async def read_all(
                        response: Response, 
                        session: AsyncSession = Depends(session)
                    ):
        """
        Получение списка объектов из БД.
        """
        @http_handler
        async def handler():
            return await crud.read_all(
                    session=session 
                )
        return await handler()

    @router.put(f'{api}/{{id}}', response_model=WithId)
    async def update(
                    response: Response, 
                    object: schema,
                    id: int,
                    session: AsyncSession = Depends(session)
                ):
        """
        Обновление информации о объекте.
        """
        @http_handler
        async def handler():
            return await crud.update(
                    session=session,
                    id=id,
                    object=object 
                )
        return await handler()

    @router.delete(f'{api}/{{id}}', response_model=Dict[str, str])
    async def delete(
                    response: Response, 
                    id: int,
                    session: AsyncSession = Depends(session)
                ):
        """
        Удаление объекта.
        """
        @http_handler
        async def handler():
            return await crud.delete(
                session=session,
                id=id 
            )
        await handler()
        return {'Message':'delete successful'}
    
    return router