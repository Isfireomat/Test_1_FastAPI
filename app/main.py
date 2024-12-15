from fastapi import FastAPI
from app.routers.api_routers import author_router, book_router, \
                                    borrow_router

app: FastAPI = FastAPI(title='Test_1_FastAPI')

app.include_router(author_router, prefix="/api", tags=["Authors"])
app.include_router(book_router, prefix="/api", tags=["Books"])
app.include_router(borrow_router, prefix="/api", tags=["Borrows"])
