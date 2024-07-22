from fastapi import APIRouter

from app.api.v1.endpoints import books, users, genres, booking

api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router.include_router(booking.router, prefix="/bookings", tags=["bookings"])
