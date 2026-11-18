
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_similar_chunks
from app.services.llm_service import generate_answer

from app.services.redis_service import (
    get_chat_history,
    save_chat_message
)


def ask_question(
    question: str,
    session_id: str | None = None
) -> dict:
    """
    Answer questions using document retrieval and Redis chat memory.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Retrieve previous conversation messages
    chat_history = []

    if session_id:
        chat_history = get_chat_history(session_id)

    # Step 2: Generate question embedding
    query_embedding = generate_embedding(question)

    # Step 3: Search relevant document chunks
    search_results = search_similar_chunks(
        query_embedding=query_embedding,
        limit=3
    )

    # Step 4: Prepare document context
    context = "\n\n".join(
        result["text"] for result in search_results
    )

    # Step 5: Generate answer using Gemini
    if search_results:
        answer = generate_answer(
            question=question,
            context=context,
            chat_history=chat_history
        )
    else:
        answer = "No relevant information found in uploaded documents."

    # Step 6: Prepare response
    result = {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "filename": item["filename"],
                "score": item["score"]
            }
            for item in search_results
        ]
    }

    # Step 7: Save conversation in Redis
    if session_id:
        save_chat_message(session_id, "user", question)
        save_chat_message(session_id, "assistant", answer)

    return result
