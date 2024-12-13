from typing import Union, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from app.data_base import get_session
from app.models import Book, Borrow,Author
from datetime import date
from pydantic import BaseModel

class CRUD:
    def __init__(self, model):
        self.__model = model
    
    async def create(self, session: AsyncSession, object: BaseModel):
        stmt = insert(self.__model).values(**object.model_dump())\
            .returning(*self.__model.__table__.columns)
        result = await session.execute(stmt)
        return result.fetchone()
    
    async def read(self, session: AsyncSession, id:int):
        stmt = select(self.__model).where(self.__model.id==id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def read_all(self, session: AsyncSession):
        stmt = select(self.__model)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(self, session: AsyncSession, id: int, object):
        if hasattr(object,'id'):
            object.id=id
        stmt = update(self.__model).where(self.__model.id==id)\
               .values(**object.model_dump())\
               .returning(*self.__model.__table__.columns)
        result = await session.execute(stmt)
        return result.fetchone()

    async def delete(self, session: AsyncSession, id:int):
        stmt = select(self.__model).where(self.__model.id == id)
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            return False
        stmt = delete(self.__model).where(self.__model.id==id)
        await session.execute(stmt)
        return True