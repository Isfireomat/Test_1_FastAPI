from fastapi import FastAPI
from app.data_base import create_start_table
import asyncio
from app.routers.CRUD_routers import author_router, book_router, borrow_router

app:FastAPI=FastAPI(title='Test_1_FastAPI')

app.include_router(author_router, prefix="/api", tags=["Authors"])
app.include_router(book_router, prefix="/api", tags=["Books"])
app.include_router(borrow_router, prefix="/api", tags=["Borrows"])
# app.include_router(book_router, prefix="/api/books", tags=["Books"])
# app.include_router(borrow_router,prefix="/api/borrows", tags=["Borrows"])
