
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag_service import ask_question

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Ask a question about uploaded documents."
    )

    session_id: str | None = Field(
        default=None,
        description="Conversation ID for remembering previous messages."
    )


@router.post("/ask")
def chat_with_document(request: ChatRequest):
    try:
        # Create a new session if one was not provided
        session_id = request.session_id or str(uuid4())

        result = ask_question(
            question=request.question,
            session_id=session_id
        )

        result["session_id"] = session_id

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question."
        ) from exc
