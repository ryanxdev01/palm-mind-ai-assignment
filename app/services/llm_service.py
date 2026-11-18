
import os
import json

from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=GEMINI_API_KEY)



def generate_answer(
    question: str,
    context: str,
    chat_history: list[dict] | None = None
) -> str:
    """Generate an answer using document context and chat history."""

    history_text = ""

    if chat_history:
        history_text = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in chat_history
        )

    prompt = f"""
You are a helpful document assistant.

Use the conversation history to understand follow-up questions.
Use the provided document context to answer questions about the documents.

If the answer is not available in the document context,
say: "I could not find this information in the uploaded document."

Conversation History:
{history_text}

Document Context:
{context}

Current Question:
{question}

Provide a clear and helpful answer.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text or "Sorry, I could not generate an answer."


def extract_booking_details(message: str) -> dict:
    """Extract interview booking details from a natural language message."""

    today = date.today().isoformat()

    prompt = f"""
You are an interview booking assistant.

Extract these details from the user's message:
- name
- email
- interview_date
- interview_time

Today's date is {today}.

Rules:
1. Return only valid JSON.
2. Use YYYY-MM-DD for interview_date.
3. Use 24-hour HH:MM:SS format for interview_time.
4. Convert relative dates such as tomorrow into an actual date.
5. If a detail is missing or unclear, return null for that field.
6. Never invent information.

Required JSON format:
{{
    "name": "John Smith",
    "email": "john@gmail.com",
    "interview_date": "2026-11-25",
    "interview_time": "10:00:00"
}}

User message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError("Gemini could not extract booking details.")

    return json.loads(response.text)

