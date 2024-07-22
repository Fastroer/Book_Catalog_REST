from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate

class CRUDGenre:
    """
    A class to handle CRUD operations for the Genre model.
    """

    async def create(self, db: AsyncSession, *, obj_in: GenreCreate) -> Genre:
        """
        Create a new genre entry in the database.

        Args:
            db (AsyncSession): The database session.
            obj_in (GenreCreate): The genre data to be created.

        Returns:
            Genre: The created genre object.

        Raises:
            ValueError: If there's a database error during the operation.
        """
        try:
            db_obj = Genre(name=obj_in.name)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error creating genre: {str(e)}")

    async def get(self, db: AsyncSession, id: int) -> Optional[Genre]:
        """
        Retrieve a genre by its ID.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the genre to retrieve.

        Returns:
            Optional[Genre]: The retrieved genre object, or None if not found.

        Raises:
            ValueError: If there's a database error during the operation.
        """
        try:
            result = await db.execute(select(Genre).filter(Genre.id == id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving genre: {str(e)}")

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[Genre]:
        """
        Retrieve multiple genres with pagination.

        Args:
            db (AsyncSession): The database session.
            skip (int): Number of records to skip (default is 0).
            limit (int): Maximum number of records to return (default is 10).

        Returns:
            List[Genre]: A list of genre objects.

        Raises:
            ValueError: If there's a database error during the operation.
        """
        try:
            result = await db.execute(select(Genre).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving genres: {str(e)}")

    async def update(self, db: AsyncSession, *, db_obj: Genre, obj_in: GenreUpdate) -> Genre:
        """
        Update an existing genre in the database.

        Args:
            db (AsyncSession): The database session.
            db_obj (Genre): The existing genre object to be updated.
            obj_in (GenreUpdate): The new data to update the genre with.

        Returns:
            Genre: The updated genre object.

        Raises:
            ValueError: If there's a database error during the operation.
        """
        try:
            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error updating genre: {str(e)}")

    async def remove(self, db: AsyncSession, *, id: int) -> Genre:
        """
        Remove a genre from the database.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the genre to remove.

        Returns:
            Genre: The removed genre object, or raises an exception if not found.

        Raises:
            ValueError: If the genre is not found or there's a database error during the operation.
        """
        try:
            result = await db.execute(select(Genre).filter(Genre.id == id))
            db_obj = result.scalars().first()
            if not db_obj:
                raise ValueError("Genre not found")
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error deleting genre: {str(e)}")

crud_genre = CRUDGenre()
