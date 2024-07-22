import asyncio
import random
from faker import Faker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import async_session, Base
from app.models.book import Book
from app.models.booking import Booking
from app.models.genre import Genre
from app.models.user import User

fake = Faker()

async def populate_database():
    async with async_session() as session:
        users = [
            User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                avatar=fake.image_url()
            ) for _ in range(20)
        ]
        
        genres = [
            Genre(
                name=fake.word()
            ) for _ in range(20)
        ]
        
        books = [
            Book(
                title=fake.sentence(),
                price=round(random.uniform(5.0, 50.0), 2),
                pages=random.randint(100, 500),
                author=users[random.randint(0, 19)]
            ) for _ in range(20)
        ]
        
        bookings = [
            Booking(
                book=books[random.randint(0, 19)],
                user=users[random.randint(0, 19)],
                start_time=fake.date_time_this_year(),
                end_time=fake.date_time_this_year(),
                active=random.choice([True, False])
            ) for _ in range(20)
        ]
        
        async with session.begin():
            session.add_all(users)
            session.add_all(genres)
            session.add_all(books)
            session.add_all(bookings)

            for book in books:
                num_genres = random.randint(1, 5)
                selected_genres = random.sample(genres, num_genres)
                book.genres.extend(selected_genres)

if __name__ == "__main__":
    asyncio.run(populate_database())
