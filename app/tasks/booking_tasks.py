from datetime import datetime, timedelta
from sqlalchemy.future import select
from app.core.init_db import async_session
from app.models.book import Book
from app.models.user import User
from app.models.genre import Genre
from app.models.booking import Booking
from app.core.celery_app import celery_app
import asyncio

@celery_app.task(name='check_bookings')
def check_bookings():
    """
    Celery task that triggers the `update_bookings` coroutine to deactivate expired bookings.

    This function uses Celery's task decorator to schedule periodic checks for expired bookings. 
    It runs the `update_bookings` coroutine to handle the asynchronous operations.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_bookings())

async def update_bookings():
    """
    Asynchronous coroutine to update and deactivate expired bookings.

    This coroutine connects to the database, retrieves all active bookings that have expired (i.e., 
    their end time is before the current time), and marks them as inactive. The changes are then 
    committed to the database.
    """
    async with async_session() as session:
        now = datetime.utcnow() + timedelta(hours=3)
        result = await session.execute(
            select(Booking).filter(Booking.end_time < now, Booking.active == True)
        )
        expired_bookings = result.scalars().all()
        for booking in expired_bookings:
            booking.active = False
        await session.commit()
