from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base Pydantic model for user data, used as a foundation for creating and updating users.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        avatar (str): The URL or path to the user's avatar image.
    """
    first_name: str
    last_name: str
    avatar: str

class UserCreate(UserBase):
    """
    Pydantic model for creating a new user. Extends `UserBase` without adding new fields.

    Inherits all attributes from `UserBase`.
    """
    pass

class UserUpdate(UserBase):
    """
    Pydantic model for updating an existing user. Extends `UserBase` without adding new fields.

    Inherits all attributes from `UserBase`.
    """
    pass

class User(UserBase):
    """
    Pydantic model representing a user with an ID. Extends `UserBase`.

    Attributes:
        id (int): The unique identifier for the user.
    """
    id: int

    class Config:
        """
        Configuration for the Pydantic model.
        """
        from_attributes = True
