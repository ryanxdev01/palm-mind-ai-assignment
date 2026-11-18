
from datetime import date, time

from pydantic import BaseModel, EmailStr, Field


class BookingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=5,
        description="Natural language interview booking request."
    )


class BookingDetails(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    interview_date: date
    interview_time: time
