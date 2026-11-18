# Palm Mind AI – Document Chatbot & Interview Booking API

An AI-powered backend application built with FastAPI. It allows users to upload PDF and TXT documents, ask questions using Retrieval-Augmented Generation (RAG), maintain multi-turn conversations, and book interviews using natural language.

## Features

- Upload PDF and TXT documents.
- Extract text from uploaded documents.
- Support fixed-size and recursive character chunking.
- Generate text embeddings using Sentence Transformers.
- Store document vectors in Qdrant.
- Save document metadata and interview bookings using SQLAlchemy and SQLite.
- Answer document-related questions using a custom RAG pipeline and Gemini.
- Maintain conversation history using Redis.
- Extract interview booking details from natural language using Gemini.
- Provide interactive API documentation through Swagger UI.

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Qdrant
- Redis
- Google Gemini API
- Sentence Transformers
- Pydantic

## Project Structure

```text
palm_mind_assignment/
├── app/
│   ├── api/
│   ├── database/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── __init__.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd palm_mind_assignment
```

### 2. Create a virtual environment

Python 3.12 is recommended.

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your Gemini API key and Redis connection URL:

```env
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6380/0
```

Do not upload your actual `.env` file or API key to GitHub.

### 5. Start Redis

Make sure Docker Desktop is running, then start a Redis container:

```bash
docker run -d --name palm-mind-redis -p 6380:6379 redis
```

If the container already exists, start it with:

```bash
docker start palm-mind-redis
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/ingestion/upload` | Upload and process PDF/TXT documents |
| POST | `/api/v1/chat/ask` | Ask questions about uploaded documents |
| POST | `/api/v1/booking/book` | Book interviews using natural language |

## Notes

- Qdrant uses local persistent storage.
- SQLite stores document metadata and interview booking records.
- Redis stores conversation history.
- A valid Gemini API key is required for LLM-powered features.
- This project provides backend APIs and does not include a frontend interface.

## Author

Developed as a technical assignment for a Backend Developer role.