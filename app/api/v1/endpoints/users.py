from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.crud_user import crud_user
from app.schemas import user
from app.core.init_db import get_session

router = APIRouter()

@router.post("/", response_model=user.User, status_code=201)
async def create_user(
    user_in: user.UserCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new user.

    Args:
        user_in (user.UserCreate): The user data to create.
        db (AsyncSession): The database session dependency.

    Returns:
        user.User: The created user.

    Raises:
        HTTPException: If the user could not be created.
    """
    try:
        user = await crud_user.create(db=db, obj_in=user_in)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[user.User])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a list of users.

    Args:
        skip (int): The number of items to skip. Defaults to 0.
        limit (int): The maximum number of items to return. Defaults to 10.
        db (AsyncSession): The database session dependency.

    Returns:
        List[user.User]: A list of users.

    Raises:
        HTTPException: If an error occurs while retrieving users.
    """
    try:
        users = await crud_user.get_multi(db=db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=user.User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (AsyncSession): The database session dependency.

    Returns:
        user.User: The requested user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user.User)
async def update_user(
    user_id: int,
    user_in: user.UserUpdate,
    db: AsyncSession = Depends(get_session)
):
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user_in (user.UserUpdate): The updated user data.
        db (AsyncSession): The database session dependency.

    Returns:
        user.User: The updated user.

    Raises:
        HTTPException: If the user is not found or if an error occurs during the update.
    """
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user = await crud_user.update(db=db, db_obj=user, obj_in=user_in)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", response_model=user.User)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (AsyncSession): The database session dependency.

    Returns:
        user.User: The deleted user.

    Raises:
        HTTPException: If the user is not found or if an error occurs during deletion.
    """
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user = await crud_user.remove(db=db, id=user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
