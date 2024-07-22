from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.init_db import Base

class Booking(Base):
    """
    SQLAlchemy model representing a booking.

    Attributes:
        id (int): The unique identifier for the booking.
        book_id (int): Foreign key referencing the book being booked.
        user_id (int): Foreign key referencing the user who made the booking.
        start_time (datetime): The start time of the booking.
        end_time (datetime): The end time of the booking.
        active (bool): Indicates whether the booking is currently active.
        book (relationship): A one-to-one relationship with Book.
        user (relationship): A one-to-one relationship with User.
    """
    __tablename__ = 'booking'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    start_time = Column(DateTime(timezone=False))
    end_time = Column(DateTime(timezone=False))
    active = Column(Boolean, default=True)
    
    book = relationship('Book')
    user = relationship('User')
