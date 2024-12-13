from datetime import date
from pydantic import BaseModel, Field, model_validator
from typing import Optional
    
class AuthorSchema(BaseModel):
    name: str = Field(
        min_length=1, 
        max_length=64
        )
    surname: str = Field(
        min_length=1, 
        max_length=64
        )
    birthday: date
    
    class Config:
        from_attributes = True
        
class BookSchema(BaseModel):
    title: str = Field(
        min_length=1, 
        max_length=128
        )
    description: str = Field(
        max_length=1024
        )
    author_id: int = Field(
        ge=0
        )
    count_available: int = Field(
        ge=0
        )
    
    class Config:
        from_attributes = True

class BorrowSchema(BaseModel):
    book_id: int = Field(
        ge=0
        )
    reader_name: str = Field(
        min_length=1, 
        max_length=64
        )
    date_borrow: date
    return_date: Optional[date] = None

    @model_validator(mode='before')
    def check_dates(cls, values):
        print("!",values)
        date_borrow = values.date_borrow
        return_date = values.return_date
        if date_borrow and return_date and date_borrow > return_date:
            raise ValueError(
                '''
                The refund date cant be longer 
                for the date of borrow
                '''
                )
        return values

    class Config:
        from_attributes = True


class BorrowCreateSchema(BaseModel):
    book_id: int = Field(
        ge=0
        )
    reader_name: str = Field(
        min_length=1, 
        max_length=64
        )
    date_borrow: date

class ReturnDateSchema(BaseModel):
    return_date: date
    