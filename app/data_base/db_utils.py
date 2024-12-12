from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from data_base import get_session
from models import Book, Borrow, BorrowCreateSchema

async def get_book_by_id(
                session: AsyncSession, 
                id: int
            ):
    stmt = select(Book).where(Book.id==id)
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
    result = session.execute(stmt)
    book = result.fetchone()
    
    return book[0] if book else None