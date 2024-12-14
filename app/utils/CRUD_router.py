from typing import Dict, Optional, Union, List, Type, TypeVar
from pydantic import BaseModel
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.data_base import get_session, CRUD
from app.models import Author, Book, Borrow, \
                   AuthorSchema, BookSchema, BorrowSchema
from functools import wraps


def router_update(router_set):
    router_dict = []
    routers = []
    for router in router_set.routes[::-1]:
        if {f"{router.path}": router.methods} not in router_dict:
            router_dict.append({f"{router.path}": router.methods})
            routers.append(router)
    router_set.routes = routers[::-1]
    
def http_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            object = await func(*args, **kwargs)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f'{e}'
            )
        if not object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{object}"
                )
        return object
    return wrapper

T = TypeVar("T", bound=BaseModel)    
class Id:
        id: Optional[int] = None 
        
def create_CRUD_router(
        model, 
        schema: Type[T],
        api: str,
        session: AsyncSession
    ):
    
    crud = CRUD(model=model)
    router = APIRouter()
    
    
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