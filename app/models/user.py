from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.init_db import Base

class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        avatar (str): The URL or path to the user's avatar image.
        books (relationship): A one-to-many relationship with Book.
    """
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    avatar = Column(String, index=True)
    
    books = relationship('Book', back_populates='author')
