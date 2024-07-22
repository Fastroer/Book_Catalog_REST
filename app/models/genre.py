from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.init_db import Base
from app.models.book import book_genre_association

class Genre(Base):
    """
    SQLAlchemy model representing a genre.

    Attributes:
        id (int): The unique identifier for the genre.
        name (str): The name of the genre.
        books (relationship): A many-to-many relationship with Book.
    """
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    books = relationship('Book', secondary=book_genre_association, back_populates='genres')
