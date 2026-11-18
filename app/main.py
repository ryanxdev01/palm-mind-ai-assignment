
from fastapi import FastAPI

from app.api.booking import router as booking_router
from app.api.ingestion import router as ingestion_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="Palm Mind AI Assignment",
    description="AI-powered Document Chatbot and Interview Booking API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Palm Mind AI Assignment",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(
    ingestion_router,
    prefix="/api/v1/ingestion",
    tags=["Document Ingestion"]
)

app.include_router(
    chat_router,
    prefix="/api/v1/chat",
    tags=["Conversational RAG"]
)

app.include_router(
    booking_router,
    prefix="/api/v1/booking",
    tags=["Interview Booking"]
)
