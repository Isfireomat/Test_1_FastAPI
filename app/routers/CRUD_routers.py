from typing import Dict, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.data_base import get_session
from app.models import Author, Book, Borrow, \
                   AuthorSchema, BookSchema, BorrowSchema, \
                   BorrowCreateSchema, ReturnDateSchema
from app.utils import create_CRUD_router, Id, router_update
from app.data_base import CRUD

author_router: APIRouter = create_CRUD_router(
    model=Author,
    schema=AuthorSchema,
    api='/authors',
    session=get_session
    )

book_router: APIRouter = create_CRUD_router(
    model=Book,
    schema=BookSchema,
    api='/books',
    session=get_session
    )

borrow_router: APIRouter = create_CRUD_router(
    model=Borrow,
    schema=BorrowSchema,
    api='/borrows',
    session=get_session
    )

borrow_crud = CRUD(model=Borrow)
book_crud = CRUD(model=Book)
class BorrowSchemaWithId(BorrowSchema, Id):
    class Config:
        from_attributes = True


@borrow_router.post('/borrows', response_model=BorrowSchemaWithId)
async def create(
                response: Response, 
                borrow: BorrowCreateSchema,
                session: AsyncSession = Depends(get_session)
            ):
    '''
    Создание записи о выыдаче книги (POST /borrows).
    
    Проверять наличие доступных экземпляров книги при создании записи 
    о выдаче.
    
    Уменьшать количество доступных экземпляров книги при выдаче.
    
    При попытке выдать недоступную книгу возвращать соответствующую ошибку.
    '''
    try:
        book = await book_crud.read(
                                session=session,
                                id=borrow.book_id 
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

        book.count_available -= 1 
        book = await book_crud.update(
            session=session,
            id=book.id,
            object=BookSchema.model_validate(book)
        )
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book barrow is bad"
            )
        
        borrow: Optional[Borrow] = await borrow_crud.create(
                                                session=session,
                                                object=borrow 
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

@borrow_router.patch('/borrows/{id}/return', response_model=BorrowSchemaWithId)
async def update(
                    response: Response,
                    id: int,
                    return_date: ReturnDateSchema,
                    session: AsyncSession = Depends(get_session)
                ):
    '''
    Завершение выдачи (PATCH /borrows/{id}/return) 
    с указанием даты возврата.
    
    Увеличивать при возврате
    '''
    
    borrow = await borrow_crud.read(
        session=session,
        id=id
    )

    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="borrow is not exists"
        )
    
    if borrow.return_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="borrow have return"
        )
    try:
        book: Book = await book_crud.read(
            session=session,
            id=borrow.book_id
        ) 
        book.count_available += 1 
        book = await book_crud.update(
            session=session,
            id=book.id,
            object=BookSchema.model_validate(book)
        )
        if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book barrow is bad"
            )
    
        borrow = await borrow_crud.update(
                                        session=session,
                                        id=id,
                                        object=return_date
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

router_update(router_set=borrow_router)
