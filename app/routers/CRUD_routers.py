from fastapi_crudrouter import SQLAlchemyCRUDRouter
from data_base import get_session
from models import Author, Book, Borrow

author_router = SQLAlchemyCRUDRouter(
    db_model=Author,
    db=get_session()   
)