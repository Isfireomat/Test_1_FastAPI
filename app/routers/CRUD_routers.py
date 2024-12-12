from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from data_base import get_session, get_book_by_id, create_borrow
from models import Author, Book, Borrow, \
                   AuthorSchema, BookSchema, BorrowSchema, \
                   BorrowCreateSchema

author_router = SQLAlchemyCRUDRouter(
    schema=AuthorSchema,
    db_model=Author,
    db=get_session()   
)

book_router = SQLAlchemyCRUDRouter(
    schema=BookSchema,
    db_model=Book,
    db=get_session()   
)

borrow_router = SQLAlchemyCRUDRouter(
    schema=BorrowSchema,
    db_model=Borrow,
    db=get_session()   
)

@borrow_router.post('/borrows', routing_model=BorrowSchema)
async def borrow_create(
                        response: Response, 
                        borrow: BorrowCreateSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    '''
    Создание записи о выдаче книги (POST /borrows).
    
    Проверять наличие доступных экземпляров книги при создании записи 
    о выдаче.
    
    Уменьшать количество доступных экземпляров книги при выдаче 
    и увеличивать при возврате.
    
    При попытке выдать недоступную книгу возвращать соответствующую ошибку.
    '''

    book = await get_book_by_id(
                                id=borrow.book_id, 
                                session=session
                            )
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book is not exists"
        )
    
    if book.count_available <= 0: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Book is not available"
        )
    
    borrow: Optional[Borrow] = create_borrow(
                                            borrow=borrow, 
                                            session=session
                                        )
    if borrow is None: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="borrow is bad"
        )
    
    return borrow