from typing import List, Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from app.models.booking import Booking
from app.models.book import Book
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate

class CRUDBooking:
    """
    A class to handle CRUD operations for the Booking model.
    """

    async def create(self, db: AsyncSession, *, obj_in: BookingCreate) -> Optional[Booking]:
        """
        Create a new booking entry in the database.

        Args:
            db (AsyncSession): The database session.
            obj_in (BookingCreate): The booking data to be created.

        Returns:
            Optional[Booking]: The created booking object, or None if the booking overlaps with an existing active booking.

        Raises:
            ValueError: If the start time is not before the end time, or if the book or user does not exist.
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            if obj_in.start_time >= obj_in.end_time:
                raise ValueError("Start time must be before end time")

            book_query = select(Book).filter(Book.id == obj_in.book_id)
            book_result = await db.execute(book_query)
            book = book_result.scalars().first()
            if not book:
                raise ValueError("Book with given ID does not exist")
            
            user_query = select(User).filter(User.id == obj_in.user_id)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()
            if not user:
                raise ValueError("User with given ID does not exist")

            existing_bookings_query = select(Booking).filter(
                and_(
                    Booking.book_id == obj_in.book_id,
                    Booking.end_time > obj_in.start_time,
                    Booking.start_time < obj_in.end_time,
                    Booking.active == True
                )
            )
            existing_bookings_result = await db.execute(existing_bookings_query)
            if existing_bookings_result.scalars().first():
                return None

            db_obj = Booking(
                book_id=obj_in.book_id,
                user_id=obj_in.user_id,
                start_time=obj_in.start_time,
                end_time=obj_in.end_time,
                active=obj_in.active
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")
        except ValueError as e:
            await db.rollback()
            raise Exception(f"Validation error: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise Exception(f"Unexpected error occurred: {str(e)}")

    async def get(self, db: AsyncSession, id: int) -> Optional[Booking]:
        """
        Retrieve a booking by its ID.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the booking to retrieve.

        Returns:
            Optional[Booking]: The retrieved booking object, or None if not found.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            result = await db.execute(select(Booking).filter(Booking.id == id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[Booking]:
        """
        Retrieve multiple bookings with pagination.

        Args:
            db (AsyncSession): The database session.
            skip (int): Number of records to skip (default is 0).
            limit (int): Maximum number of records to return (default is 10).

        Returns:
            List[Booking]: A list of booking objects.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            result = await db.execute(select(Booking).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")

    async def update(self, db: AsyncSession, *, db_obj: Booking, obj_in: BookingUpdate) -> Optional[Booking]:
        """
        Update an existing booking in the database.

        Args:
            db (AsyncSession): The database session.
            db_obj (Booking): The existing booking object to be updated.
            obj_in (BookingUpdate): The new data to update the booking with.

        Returns:
            Optional[Booking]: The updated booking object, or None if the updated booking overlaps with an existing active booking.

        Raises:
            ValueError: If the start time is not before the end time, or if the book or user does not exist.
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            if obj_in.start_time and obj_in.end_time and obj_in.start_time >= obj_in.end_time:
                raise ValueError("Start time must be before end time")

            book_query = select(Book).filter(Book.id == obj_in.book_id)
            book_result = await db.execute(book_query)
            book = book_result.scalars().first()
            if not book:
                raise ValueError("Book with given ID does not exist")

            user_query = select(User).filter(User.id == obj_in.user_id)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()
            if not user:
                raise ValueError("User with given ID does not exist")

            start_time_naive = obj_in.start_time or db_obj.start_time
            end_time_naive = obj_in.end_time or db_obj.end_time

            if start_time_naive or end_time_naive:
                existing_bookings_query = select(Booking).filter(
                    and_(
                        Booking.book_id == db_obj.book_id,
                        Booking.id != db_obj.id,
                        Booking.end_time > start_time_naive,
                        Booking.start_time < end_time_naive,
                        Booking.active == True
                    )
                )
                existing_bookings_result = await db.execute(existing_bookings_query)
                if existing_bookings_result.scalars().first():
                    return None

            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)
            
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")
        except ValueError as e:
            await db.rollback()
            raise Exception(f"Validation error: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise Exception(f"Unexpected error occurred: {str(e)}")

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[Booking]:
        """
        Remove a booking from the database.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the booking to remove.

        Returns:
            Optional[Booking]: The removed booking object, or None if not found.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            result = await db.execute(select(Booking).filter(Booking.id == id))
            db_obj = result.scalars().first()
            if not db_obj:
                return None
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")

    async def cancel(self, db: AsyncSession, *, id: int) -> Optional[Booking]:
        """
        Cancel a booking by marking it as inactive and adjusting the end time.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the booking to cancel.

        Returns:
            Optional[Booking]: The updated (canceled) booking object, or None if not found.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
            Exception: For any unexpected errors.
        """
        try:
            result = await db.execute(select(Booking).filter(Booking.id == id))
            db_obj = result.scalars().first()
            if not db_obj:
                return None
            
            db_obj.active = False
            db_obj.end_time = datetime.utcnow() + timedelta(hours=3)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")

crud_booking = CRUDBooking()
