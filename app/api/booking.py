
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database.connection import get_db
from app.database.crud import create_interview_booking
from app.schemas.booking import BookingRequest, BookingDetails
from app.services.llm_service import extract_booking_details

router = APIRouter()


@router.post("/book")
def book_interview(
    request: BookingRequest,
    db: Session = Depends(get_db)
):
    try:
        # Step 1: Extract details using Gemini
        extracted_data = extract_booking_details(request.message)

        # Step 2: Validate extracted details
        booking_details = BookingDetails(**extracted_data)

        # Step 3: Save booking in SQLite
        booking = create_interview_booking(
            db=db,
            name=booking_details.name,
            email=booking_details.email,
            interview_date=booking_details.interview_date,
            interview_time=booking_details.interview_time
        )

        return {
            "message": "Interview booked successfully.",
            "booking_id": booking.id,
            "name": booking.name,
            "email": booking.email,
            "interview_date": booking.interview_date,
            "interview_time": booking.interview_time,
            "status": booking.status
        }

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail="Missing or invalid interview booking details."
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to process interview booking."
        ) from exc
