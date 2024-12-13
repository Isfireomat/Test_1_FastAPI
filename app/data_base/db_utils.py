from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models import Book, Borrow
from datetime import date

async def update_return_date_borrow(
                                session: AsyncSession,
                                borrow: Borrow,
                                return_date: date = date.today()
                            ):
    stmt = update(Borrow).where(Borrow.id==borrow.id)\
           .values(return_date=return_date).returning(Borrow)
    result = await session.execute(stmt)
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
    book = result.fetchone()
    return book[0] if book else None
 