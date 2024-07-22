from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.crud_genre import crud_genre
from app.schemas import genre
from app.core.init_db import get_session

router = APIRouter()

@router.post("/", response_model=genre.Genre, status_code=201)
async def create_genre(
    genre_in: genre.GenreCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new genre.

    Args:
        genre_in (genre.GenreCreate): The data to create a new genre.
        db (AsyncSession): The database session dependency.

    Returns:
        genre.Genre: The created genre.

    Raises:
        HTTPException: If there is an error creating the genre.
    """
    try:
        genre = await crud_genre.create(db=db, obj_in=genre_in)
        return genre
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[genre.Genre])
async def read_genres(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a list of genres.

    Args:
        skip (int): Number of items to skip. Defaults to 0.
        limit (int): Maximum number of items to return. Defaults to 10.
        db (AsyncSession): The database session dependency.

    Returns:
        List[genre.Genre]: A list of genres.

    Raises:
        HTTPException: If there is an error retrieving the genres.
    """
    try:
        genres = await crud_genre.get_multi(db=db, skip=skip, limit=limit)
        return genres
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{genre_id}", response_model=genre.Genre)
async def read_genre(
    genre_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific genre by ID.

    Args:
        genre_id (int): The ID of the genre to retrieve.
        db (AsyncSession): The database session dependency.

    Returns:
        genre.Genre: The requested genre.

    Raises:
        HTTPException: If the genre is not found or if there is an error retrieving it.
    """
    try:
        genre = await crud_genre.get(db=db, id=genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return genre
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{genre_id}", response_model=genre.Genre)
async def update_genre(
    genre_id: int,
    genre_in: genre.GenreUpdate,
    db: AsyncSession = Depends(get_session)
):
    """
    Update an existing genre.

    Args:
        genre_id (int): The ID of the genre to update.
        genre_in (genre.GenreUpdate): The updated genre data.
        db (AsyncSession): The database session dependency.

    Returns:
        genre.Genre: The updated genre.

    Raises:
        HTTPException: If the genre is not found or if there is an error updating it.
    """
    try:
        genre = await crud_genre.get(db=db, id=genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        genre = await crud_genre.update(db=db, db_obj=genre, obj_in=genre_in)
        return genre
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{genre_id}", response_model=genre.Genre)
async def delete_genre(
    genre_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a genre by ID.

    Args:
        genre_id (int): The ID of the genre to delete.
        db (AsyncSession): The database session dependency.

    Returns:
        genre.Genre: The deleted genre.

    Raises:
        HTTPException: If the genre is not found or if there is an error deleting it.
    """
    try:
        genre = await crud_genre.get(db=db, id=genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        genre = await crud_genre.remove(db=db, id=genre_id)
        return genre
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
