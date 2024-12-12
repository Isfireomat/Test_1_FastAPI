from typing import Dict, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from data_base import get_session, get_book_by_id, create_borrow, \
                      get_borrow_by_id, update_return_date_borrow, \
                      update_book_count_available_by_id
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
async def borrows_create(
                        response: Response, 
                        borrow: BorrowCreateSchema,
                        session: AsyncSession = Depends(get_session)
                    ):
    '''
    Создание записи о выдаче книги (POST /borrows).
    
    Проверять наличие доступных экземпляров книги при создании записи 
    о выдаче.
    
    Уменьшать количество доступных экземпляров книги при выдаче.
    
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
    
    try:
        async with session.begin():
            book = await update_book_count_available_by_id(
                                                session=session,
                                                id=book.id,
                                                count=-1
                                                )
        
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book barrow is bad"
                )
            
            borrow: Optional[Borrow] = await create_borrow(
                                                    borrow=borrow, 
                                                    session=session
                                                )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )

    if borrow is None: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="borrow is bad"
        )
    
    return borrow

@book_router.patch('/borrows/{id}/return', routing_model=BorrowSchema)
async def borrows_return(
                    response: Response,
                    id: int,
                    return_date = Depends(),
                    session: AsyncSession = Depends(get_session)
                ):
    '''
    Завершение выдачи (PATCH /borrows/{id}/return) 
    с указанием даты возврата.
    
    Увеличивать при возврате
    '''

    if not return_date:
        return_date = date.today()
    
    borrow: Optional[Borrow] = await get_borrow_by_id(id=id)

    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="borrow is not exists"
        )
    try:
        async with session.begin():
            book = await update_book_count_available_by_id(
                                                session=session,
                                                id=book.id,
                                                count=1
                                                )
        
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book barrow is bad"
                )
        
            borrow: Optional[Borrow] = await update_return_date_borrow(
                                                                session=session,
                                                                borrow=borrow,
                                                                return_date=return_date
                                                            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="borrow is bad"
        )
    
    return borrow