from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional

class BookingBase(BaseModel):
    """
    Base Pydantic model for booking data, used as a base for creating and updating bookings.

    Attributes:
        book_id (int): The unique identifier of the book being booked.
        user_id (int): The unique identifier of the user making the booking.
        start_time (datetime): The start time of the booking in the format "HH:MM dd.mm.YYYY".
        end_time (datetime): The end time of the booking in the format "HH:MM dd.mm.YYYY".
        active (Optional[bool]): The status of the booking. Defaults to `True`. Optional.
    
    Validators:
        - `parse_datetime`: Converts `start_time` and `end_time` strings to `datetime` objects if they are in string format.
    """
    book_id: int
    user_id: int
    start_time: datetime = Field(..., example="12:00 21.07.2024")
    end_time: datetime = Field(..., example="12:00 22.07.2024")
    active: Optional[bool] = True

    @field_validator('start_time', 'end_time', mode='before')
    def parse_datetime(cls, value):
        """
        Validates and converts the `start_time` and `end_time` fields from string to `datetime` if necessary.
        
        Args:
            cls (Type[BaseModel]): The class of the model.
            value (Union[str, datetime]): The value of the field to validate.

        Returns:
            datetime: The validated and converted datetime value.

        Raises:
            ValueError: If the value cannot be parsed into a datetime object.
        """
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%H:%M %d.%m.%Y")
            except ValueError:
                raise ValueError("Time format should be HH:MM dd.mm.YYYY")
        return value

class BookingCreate(BookingBase):
    """
    Pydantic model for creating a booking. Extends `BookingBase` with no additional fields.
    """
    pass

class BookingUpdate(BookingBase):
    """
    Pydantic model for updating a booking. Extends `BookingBase` with no additional fields.
    """
    pass

class Booking(BookingBase):
    """
    Pydantic model representing a booking with an ID. Extends `BookingBase`.

    Attributes:
        id (int): The unique identifier for the booking.
    """
    id: int

    class Config:
        """
        Configuration for the Pydantic model.
        """
        from_attributes = True
