from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from app.models.book import Book
from app.models.user import User
from app.models.genre import Genre
from app.schemas.book import BookCreate, BookUpdate

class CRUDBook:
    """
    A class to handle CRUD operations for the Book model.
    """

    async def create(self, db: AsyncSession, *, obj_in: BookCreate) -> Book:
        """
        Create a new book entry in the database.

        Args:
            db (AsyncSession): The database session.
            obj_in (BookCreate): The book data to be created.

        Returns:
            Book: The created book object.

        Raises:
            ValueError: If the author or any genres are not found.
            SQLAlchemyError: If there's an error while creating the book.
        """
        try:
            author = await db.execute(select(User).filter(User.id == obj_in.author_id))
            author_obj = author.scalars().first()
            if not author_obj:
                raise ValueError("Author not found")

            genres = []
            if obj_in.genres:
                for genre_id in obj_in.genres:
                    genre = await db.execute(select(Genre).filter(Genre.id == genre_id))
                    genre_obj = genre.scalars().first()
                    if genre_obj:
                        genres.append(genre_obj)
                    else:
                        raise ValueError(f"Genre with id {genre_id} not found")

            db_obj = Book(
                title=obj_in.title,
                price=obj_in.price,
                pages=obj_in.pages,
                author=author_obj,
                genres=genres
            )
            db.add(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error creating book: {str(e)}")

    async def get(self, db: AsyncSession, id: int) -> Optional[Book]:
        """
        Retrieve a book by its ID.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the book to retrieve.

        Returns:
            Optional[Book]: The retrieved book object, or None if not found.

        Raises:
            SQLAlchemyError: If there's an error while retrieving the book.
        """
        try:
            result = await db.execute(select(Book).options(selectinload(Book.genres)).filter(Book.id == id))
            book = result.scalars().first()
            return book
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving book: {str(e)}")

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[Book]:
        """
        Retrieve multiple books with pagination.

        Args:
            db (AsyncSession): The database session.
            skip (int): Number of records to skip (default is 0).
            limit (int): Maximum number of records to return (default is 10).

        Returns:
            List[Book]: A list of book objects.

        Raises:
            SQLAlchemyError: If there's an error while retrieving books.
        """
        try:
            result = await db.execute(select(Book).offset(skip).limit(limit).options(selectinload(Book.genres)))
            books = result.scalars().all()
            return books
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving books: {str(e)}")

    async def update(self, db: AsyncSession, *, db_obj: Book, obj_in: BookUpdate) -> Book:
        """
        Update an existing book in the database.

        Args:
            db (AsyncSession): The database session.
            db_obj (Book): The book object to be updated.
            obj_in (BookUpdate): The new data to update the book with.

        Returns:
            Book: The updated book object.

        Raises:
            ValueError: If the author or any genres are not found.
            SQLAlchemyError: If there's an error while updating the book.
        """
        try:
            if obj_in.author_id is not None:
                author = await db.execute(select(User).filter(User.id == obj_in.author_id))
                author_obj = author.scalars().first()
                if not author_obj:
                    raise ValueError("Author not found")
                db_obj.author = author_obj

            if obj_in.genres is not None:
                genres = []
                for genre_id in obj_in.genres:
                    genre = await db.execute(select(Genre).filter(Genre.id == genre_id))
                    genre_obj = genre.scalars().first()
                    if genre_obj:
                        genres.append(genre_obj)
                    else:
                        raise ValueError(f"Genre with id {genre_id} not found")
                db_obj.genres = genres

            if obj_in.title is not None:
                db_obj.title = obj_in.title
            if obj_in.price is not None:
                db_obj.price = obj_in.price
            if obj_in.pages is not None:
                db_obj.pages = obj_in.pages

            db.add(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error updating book: {str(e)}")

    async def remove(self, db: AsyncSession, *, id: int) -> Book:
        """
        Remove a book from the database.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the book to remove.

        Returns:
            Book: The removed book object.

        Raises:
            ValueError: If the book is not found.
            SQLAlchemyError: If there's an error while deleting the book.
        """
        try:
            result = await db.execute(select(Book).filter(Book.id == id))
            db_obj = result.scalars().first()
            if not db_obj:
                raise ValueError("Book not found")
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error deleting book: {str(e)}")

    async def filter(self, db: AsyncSession, *, author: Optional[str] = None, genre: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Book]:
        """
        Filter books based on various criteria.

        Args:
            db (AsyncSession): The database session.
            author (Optional[str]): Filter books by author name.
            genre (Optional[str]): Filter books by genre name.
            min_price (Optional[float]): Filter books with price greater than or equal to this value.
            max_price (Optional[float]): Filter books with price less than or equal to this value.

        Returns:
            List[Book]: A list of books that match the criteria.

        Raises:
            SQLAlchemyError: If there's an error while filtering books.
        """
        try:
            query = select(Book).options(selectinload(Book.genres))

            if author:
                query = query.filter(
                    or_(
                        Book.author.has(first_name=author),
                        Book.author.has(last_name=author),
                        Book.author.has(avatar=author)
                    )
                )

            if genre:
                query = query.filter(Book.genres.any(name=genre))

            if min_price is not None:
                query = query.filter(Book.price >= min_price)

            if max_price is not None:
                query = query.filter(Book.price <= max_price)

            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error filtering books: {str(e)}")

crud_book = CRUDBook()
