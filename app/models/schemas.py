from typing import Optional
from datetime import date
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode='after')
    def check_dates(cls, values: BaseModel) -> BaseModel:
        date_borrow: date = values.date_borrow
        return_date: date = values.return_date
        if date_borrow and return_date and date_borrow > return_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The refund date cant be longer \
                    for the date of borrow'
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
    