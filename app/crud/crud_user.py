from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser:
    """
    A class to handle CRUD operations for the User model.
    """

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Create a new user entry in the database.

        Args:
            db (AsyncSession): The database session.
            obj_in (UserCreate): The user data to be created.

        Returns:
            User: The created user object.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
        """
        try:
            db_obj = User(
                first_name=obj_in.first_name,
                last_name=obj_in.last_name,
                avatar=obj_in.avatar
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error creating user: {str(e)}")

    async def get(self, db: AsyncSession, id: int) -> Optional[User]:
        """
        Retrieve a user by its ID.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The retrieved user object, or None if not found.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
        """
        try:
            result = await db.execute(select(User).filter(User.id == id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving user: {str(e)}")

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[User]:
        """
        Retrieve multiple users with pagination.

        Args:
            db (AsyncSession): The database session.
            skip (int): Number of records to skip (default is 0).
            limit (int): Maximum number of records to return (default is 10).

        Returns:
            List[User]: A list of user objects.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
        """
        try:
            result = await db.execute(select(User).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error retrieving users: {str(e)}")

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Update an existing user in the database.

        Args:
            db (AsyncSession): The database session.
            db_obj (User): The existing user object to be updated.
            obj_in (UserUpdate): The new data to update the user with.

        Returns:
            User: The updated user object.

        Raises:
            SQLAlchemyError: If there's a database error during the operation.
        """
        try:
            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error updating user: {str(e)}")

    async def remove(self, db: AsyncSession, *, id: int) -> User:
        """
        Remove a user from the database.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the user to remove.

        Returns:
            User: The removed user object, or raises an exception if not found.

        Raises:
            ValueError: If the user is not found.
            SQLAlchemyError: If there's a database error during the operation.
        """
        try:
            result = await db.execute(select(User).filter(User.id == id))
            db_obj = result.scalars().first()
            if not db_obj:
                raise ValueError("User not found")
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        except SQLAlchemyError as e:
            raise ValueError(f"Error deleting user: {str(e)}")

crud_user = CRUDUser()
