from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.crud_booking import crud_booking
from app.schemas.booking import Booking, BookingCreate, BookingUpdate
from app.core.init_db import get_session

router = APIRouter()

@router.post("/", response_model=Booking)
async def create_booking(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new booking.

    Args:
        booking_in (BookingCreate): The data to create a new booking.
        db (AsyncSession): The database session dependency.

    Returns:
        Booking: The created booking.

    Raises:
        HTTPException: If the booking cannot be created or if the booking is already in the specified period.
    """
    try:
        booking = await crud_booking.create(db=db, obj_in=booking_in)
        if not booking:
            raise HTTPException(status_code=400, detail="Book is already booked in the specified period")
        return booking
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Booking])
async def read_bookings(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a list of bookings.

    Args:
        skip (int): Number of items to skip. Defaults to 0.
        limit (int): Maximum number of items to return. Defaults to 10.
        db (AsyncSession): The database session dependency.

    Returns:
        List[Booking]: A list of bookings.

    Raises:
        HTTPException: If there is an error retrieving the bookings.
    """
    try:
        bookings = await crud_booking.get_multi(db=db, skip=skip, limit=limit)
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}", response_model=Booking)
async def read_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific booking by ID.

    Args:
        booking_id (int): The ID of the booking to retrieve.
        db (AsyncSession): The database session dependency.

    Returns:
        Booking: The requested booking.

    Raises:
        HTTPException: If the booking is not found or if there is an error retrieving it.
    """
    try:
        booking = await crud_booking.get(db=db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{booking_id}", response_model=Booking)
async def update_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: AsyncSession = Depends(get_session)
):
    """
    Update an existing booking.

    Args:
        booking_id (int): The ID of the booking to update.
        booking_in (BookingUpdate): The updated booking data.
        db (AsyncSession): The database session dependency.

    Returns:
        Booking: The updated booking.

    Raises:
        HTTPException: If the booking is not found, if the booking is already in the specified period, or if there is an error updating it.
    """
    try:
        booking = await crud_booking.get(db=db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        updated_booking = await crud_booking.update(db=db, db_obj=booking, obj_in=booking_in)
        if not updated_booking:
            raise HTTPException(status_code=400, detail="Book is already booked in the specified period")
        return updated_booking
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{booking_id}", response_model=Booking)
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a booking by ID.

    Args:
        booking_id (int): The ID of the booking to delete.
        db (AsyncSession): The database session dependency.

    Returns:
        Booking: The deleted booking.

    Raises:
        HTTPException: If the booking is not found or if there is an error deleting it.
    """
    try:
        booking = await crud_booking.remove(db=db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{booking_id}/cancel", response_model=Booking)
async def cancel_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Cancel a booking by ID.

    Args:
        booking_id (int): The ID of the booking to cancel.
        db (AsyncSession): The database session dependency.

    Returns:
        Booking: The canceled booking.

    Raises:
        HTTPException: If the booking is not found or if there is an error canceling it.
    """
    try:
        booking = await crud_booking.cancel(db=db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
