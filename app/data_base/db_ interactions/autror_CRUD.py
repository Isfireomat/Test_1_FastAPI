from typing import Union, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from app.data_base import get_session
from app.models import Book, Borrow,Author, BorrowCreateSchema
from datetime import date
from pydantic import BaseModel

class CRUD:
    
    schema: Type = BaseModel
    
    async def __init__(self, model: Union[Author, Book, Borrow], schema: Type[BaseModel]):
        self.__model = model
        self.__schema = schema
    
    async def create(self, session: AsyncSession, data: BaseModel):
        stmt = insert(self.__model).values(**data.model_dump())
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one_or_none()
    
    async def get(self, session: AsyncSession, id:int):
        stmt = select(self.__model).where(self.__model.id==id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, session: AsyncSession):
        stmt = select(self.__model)
        result = await session.execute(stmt)
        records = result.scalars().all()
        return [record.to_dict() for record in records]

    async def update(self, session: AsyncSession, id: int, data):
        stmt = update(self.__model).where(self.__model.id==id)\
               .values(**data.model_dump()).returning(self.__model)
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()
    

    async def delete(self, session: AsyncSession, id:int):
        stmt = delete(self.__model).where(self.__model.id==id)
        await session.execute(stmt)
        await session.commit()