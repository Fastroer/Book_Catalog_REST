from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.core.init_db import Base

book_genre_association = Table(
    'book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('genre_id', Integer, ForeignKey('genre.id'))
)

class Book(Base):
    """
    SQLAlchemy model representing a book.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        price (float): The price of the book.
        pages (int): The number of pages in the book.
        author_id (int): Foreign key referencing the user who is the author of the book.
        genres (relationship): A many-to-many relationship with Genre.
        author (relationship): A many-to-one relationship with User.
    """
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey('user.id'))
    
    genres = relationship('Genre', secondary=book_genre_association, back_populates='books')
    author = relationship('User', back_populates='books')
