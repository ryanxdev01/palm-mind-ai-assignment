
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, Time
from app.database.connection import Base


class DocumentMetadata(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
    chunking_strategy = Column(String(50), nullable=False)
    total_chunks = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    interview_date = Column(Date, nullable=False)
    interview_time = Column(Time, nullable=False)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
