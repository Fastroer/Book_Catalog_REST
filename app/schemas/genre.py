from pydantic import BaseModel

class GenreBase(BaseModel):
    """
    Base Pydantic model for genre data, used as a base for creating and updating genres.

    Attributes:
        name (str): The name of the genre.
    """
    name: str

class GenreCreate(GenreBase):
    """
    Pydantic model for creating a genre. Extends `GenreBase` with no additional fields.
    """
    pass

class GenreUpdate(GenreBase):
    """
    Pydantic model for updating a genre. Extends `GenreBase` with no additional fields.
    """
    pass

class Genre(GenreBase):
    """
    Pydantic model representing a genre with an ID. Extends `GenreBase`.

    Attributes:
        id (int): The unique identifier for the genre.
    """
    id: int

    class Config:
        """
        Configuration for the Pydantic model.
        """
        from_attributes = True
