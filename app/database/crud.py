
from sqlalchemy.orm import Session

from app.database.models import DocumentMetadata, InterviewBooking


def create_document_metadata(
    db: Session,
    filename: str,
    file_type: str,
    size_bytes: int,
    character_count: int,
    chunking_strategy: str,
    total_chunks: int
) -> DocumentMetadata:
    """Save uploaded document information in the database."""

    document = DocumentMetadata(
        filename=filename,
        file_type=file_type,
        size_bytes=size_bytes,
        character_count=character_count,
        chunking_strategy=chunking_strategy,
        total_chunks=total_chunks
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def create_interview_booking(
    db: Session,
    name: str,
    email: str,
    interview_date,
    interview_time
) -> InterviewBooking:
    """Save interview booking information in the database."""

    booking = InterviewBooking(
        name=name,
        email=email,
        interview_date=interview_date,
        interview_time=interview_time
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking
