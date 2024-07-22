from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.crud_book import crud_book
from app.schemas import book
from app.core.init_db import get_session

router = APIRouter()

@router.post("/", response_model=book.Book, status_code=201)
async def create_book(
    book_in: book.BookCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new book.

    Args:
        book_in (book.BookCreate): The data to create a new book.
        db (AsyncSession): The database session dependency.

    Returns:
        book.Book: The created book.

    Raises:
        HTTPException: If there is an error creating the book.
    """
    try:
        book = await crud_book.create(db=db, obj_in=book_in)
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[book.Book])
async def read_books(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a list of books.

    Args:
        skip (int): Number of items to skip. Defaults to 0.
        limit (int): Maximum number of items to return. Defaults to 10.
        db (AsyncSession): The database session dependency.

    Returns:
        List[book.Book]: A list of books.

    Raises:
        HTTPException: If there is an error retrieving the books.
    """
    try:
        books = await crud_book.get_multi(db=db, skip=skip, limit=limit)
        return books
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{book_id}", response_model=book.Book)
async def read_book(
    book_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific book by ID.

    Args:
        book_id (int): The ID of the book to retrieve.
        db (AsyncSession): The database session dependency.

    Returns:
        book.Book: The requested book.

    Raises:
        HTTPException: If the book is not found or if there is an error retrieving it.
    """
    try:
        book = await crud_book.get(db=db, id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{book_id}", response_model=book.Book)
async def update_book(
    book_id: int,
    book_in: book.BookUpdate,
    db: AsyncSession = Depends(get_session)
):
    """
    Update an existing book.

    Args:
        book_id (int): The ID of the book to update.
        book_in (book.BookUpdate): The updated book data.
        db (AsyncSession): The database session dependency.

    Returns:
        book.Book: The updated book.

    Raises:
        HTTPException: If the book is not found or if there is an error updating it.
    """
    try:
        book = await crud_book.get(db=db, id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        book = await crud_book.update(db=db, db_obj=book, obj_in=book_in)
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{book_id}", response_model=book.Book)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a book by ID.

    Args:
        book_id (int): The ID of the book to delete.
        db (AsyncSession): The database session dependency.

    Returns:
        book.Book: The deleted book.

    Raises:
        HTTPException: If the book is not found or if there is an error deleting it.
    """
    try:
        book = await crud_book.get(db=db, id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        book = await crud_book.remove(db=db, id=book_id)
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/filter/", response_model=List[book.Book])
async def filter_books(
    author: Optional[str] = None,
    genre: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_session)
):
    """
    Filter books based on optional query parameters.

    Args:
        author (Optional[str]): Filter books by author name.
        genre (Optional[str]): Filter books by genre.
        min_price (Optional[float]): Filter books by minimum price.
        max_price (Optional[float]): Filter books by maximum price.
        db (AsyncSession): The database session dependency.

    Returns:
        List[book.Book]: A list of filtered books.

    Raises:
        HTTPException: If there is an error filtering the books.
    """
    try:
        books = await crud_book.filter(
            db=db,
            author=author,
            genre=genre,
            min_price=min_price,
            max_price=max_price
        )
        return books
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
