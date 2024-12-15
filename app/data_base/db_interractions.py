from typing import Optional, Dict, List
from pydantic import BaseModel
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUD:
    def __init__(self, model: BaseModel) -> None:
        self.__model = model
    
    async def create(self, session: AsyncSession, object: BaseModel) -> BaseModel:
        stmt: str = insert(self.__model).values(**object.model_dump())\
            .returning(*self.__model.__table__.columns)
        result = await session.execute(stmt)
        return result.fetchone()
    
    async def read(self, session: AsyncSession, id: int) -> BaseModel:
        stmt: str = select(self.__model).where(self.__model.id==id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def read_all(self, session: AsyncSession) -> List[BaseModel]:
        stmt = select(self.__model)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(self, session: AsyncSession, id: int, object) -> BaseModel:
        stmt: str = update(self.__model).where(self.__model.id==id)\
               .values(**object.model_dump())\
               .returning(*self.__model.__table__.columns)
        result = await session.execute(stmt)
        return result.fetchone()

    async def delete(self, session: AsyncSession, id:int) -> bool:
        stmt: str = select(self.__model).where(self.__model.id == id)
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            return False
        stmt: str = delete(self.__model).where(self.__model.id==id)
        await session.execute(stmt)
        return True