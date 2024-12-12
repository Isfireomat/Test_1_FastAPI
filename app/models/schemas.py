from typing import Date
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
    birthday: Date

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

class BorrowSchema(BaseModel):
    book_id: int = Field(
        ge=0
        )
    reader_name: str = Field(
        min_length=1, 
        max_length=64
        )
    date_borrow: Date
    date_refund: Date

    @model_validator(mode='before')
    def check_dates(cls, values):
        date_borrow = values.get('date_borrow')
        date_refund = values.get('date_refund')
        if date_borrow > date_refund:
            raise ValueError(
                '''
                The refund date cant be longer 
                for the date of borrow
                '''
                )
        return values

class BorrowCreateSchema(BaseModel):
    book_id: int = Field(
        ge=0
        )
    reader_name: str = Field(
        min_length=1, 
        max_length=64
        )
    date_borrow: Date
    