from pydantic import BaseModel
from typing import List, Optional

class Genre(BaseModel):
    """
    Pydantic model representing a genre.

    Attributes:
        id (int): The unique identifier for the genre.
        name (str): The name of the genre.
    """
    id: int
    name: str

class BookBase(BaseModel):
    """
    Base Pydantic model for book data, used as a base for creating and updating books.

    Attributes:
        title (str): The title of the book.
        price (float): The price of the book.
        pages (int): The number of pages in the book.
        author_id (int): The unique identifier of the author of the book.
        genres (Optional[List[Genre]]): A list of genres associated with the book. Optional.
    """
    title: str
    price: float
    pages: int
    author_id: int
    genres: Optional[List[Genre]] = []

class BookCreate(BookBase):
    """
    Pydantic model for creating a book. Extends `BookBase` and includes genre IDs.

    Attributes:
        genres (Optional[List[int]]): A list of genre IDs associated with the book. Optional.
    """
    genres: Optional[List[int]] = []

class BookUpdate(BookBase):
    """
    Pydantic model for updating a book. Extends `BookBase` and allows partial updates.

    Attributes:
        title (Optional[str]): The title of the book. Optional.
        price (Optional[float]): The price of the book. Optional.
        pages (Optional[int]): The number of pages in the book. Optional.
        genres (Optional[List[int]]): A list of genre IDs associated with the book. Optional.
    """
    title: Optional[str] = None
    price: Optional[float] = None
    pages: Optional[int] = None
    genres: Optional[List[int]] = []

class Book(BookBase):
    """
    Pydantic model representing a book with an ID. Extends `BookBase`.

    Attributes:
        id (int): The unique identifier for the book.
    """
    id: int
    
    class Config:
        """
        Configuration for the Pydantic model.
        """
        from_attributes = True
