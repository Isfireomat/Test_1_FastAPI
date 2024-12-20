from sqlalchemy import Column, Integer, String, Date, ForeignKey, \
                       CheckConstraint
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Author(Base):
    """
    Author (Автор): id, имя, фамилия, дата рождения.
    """

    __tablename__ = 'Author'

    id = Column(
        Integer, 
        primary_key=True
    )
    name = Column(
        String(64),
        CheckConstraint('LENGTH(name) > 1',  
                        name='check_author_name_length'
                        ), 
        nullable=False
    )
    surname = Column(
        String(64),
        CheckConstraint('LENGTH(surname) > 1',
                         name='check_author_surname_length'
                        ),
        nullable=False
    )
    birthday = Column(
        Date, 
        nullable=False
    )


    class Config:
        orm_mode = True
        
class Book(Base):
    """
    Book (Книга): id, название, описание, 
    id автора, количество доступных экземпляров.  
    """

    __tablename__ = 'Book'

    id = Column(
        Integer, 
        primary_key=True
    )
    title = Column(
        String(128), 
        nullable=False
    )
    description = Column(
        String(1024), 
        nullable=True
    )
    author_id = Column(
        Integer, 
        ForeignKey('Author.id'), 
        nullable=False
    )
    count_available = Column(
        Integer,
        CheckConstraint('count_available >= 0',  
                        name='check_positive_count_available'
                        ),
        nullable=False
    )


    class Config:
        orm_mode = True


class Borrow(Base):
    """
    Borrow (Выдача): id, id книги, имя читателя, дата выдачи, 
    дата возврата.
    """

    __tablename__ = 'Borrow'

    id = Column(Integer, primary_key=True)
    book_id = Column(
        Integer, 
        ForeignKey('Book.id'), 
        nullable=False
    )
    reader_name = Column(
        String(64),          
        CheckConstraint('LENGTH(reader_name) > 1',
                         name='check_reader_name_length'
                        ), 
        nullable=False
    )
    date_borrow = Column(
        Date, 
        nullable=False
    )
    return_date = Column(
        Date, 
        CheckConstraint('return_date >= date_borrow',
                         name='check_return_date'
                        ),
        nullable=True
    )
    
    
    class Config:
        orm_mode = True
    