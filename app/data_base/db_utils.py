from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update
from data_base import get_session
from models import Book, Borrow, BorrowCreateSchema
from datetime import date

async def get_book_by_id(
                session: AsyncSession, 
                id: int
            ):
    stmt = select(Book).where(Book.id==id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_borrow_by_id(
                session: AsyncSession, 
                id: int
            ):
    stmt = select(Borrow).where(Borrow.id==id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_borrow(
                    session: AsyncSession,
                    borrow: BorrowCreateSchema
                ):
    stmt = insert(Borrow).values(
                        book_id=borrow.book_id,
                        reader_name=borrow.reader_name,
                        date_borrow=borrow.date_borrow
                    ).returning(Borrow)
    result = await session.execute(stmt)
    book = result.fetchone()
    
    return book[0] if book else None

async def update_return_date_borrow(
                                session: AsyncSession,
                                borrow: Borrow,
                                return_date: date = date.today()
                            ):
    stmt = update(Borrow).where(Borrow.id==borrow.id)\
           .values(return_date=return_date).returning(Borrow)
    result = await session.execute(stmt)
    await session.commit()
    borrow = result.fetchone()
    return borrow[0] if borrow else None

async def update_book_count_available_by_id(
                                        session: AsyncSession,
                                        id: int,
                                        count: int = 0
                                    ):
    stmt = update(Book).where(Book.id==id)\
           .values(count_available=Book.count_available+count).returning(Book)
    result = await session.execute(stmt)
    await session.commit()
    book = result.fetchone()
    return book[0] if book else None
 