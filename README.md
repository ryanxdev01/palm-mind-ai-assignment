# Palm Mind AI – Document Chatbot & Interview Booking API

An AI-powered backend application built with **FastAPI** that enables users to upload PDF and TXT documents, ask context-aware questions using Retrieval-Augmented Generation (RAG), maintain multi-turn conversations, and book interviews using natural language.

## Features

- Upload PDF and TXT documents.
- Extract text from uploaded documents.
- Support fixed-size and recursive character text chunking.
- Generate text embeddings using Sentence Transformers.
- Store document vectors in Qdrant.
- Store document metadata and interview bookings using SQLAlchemy and SQLite.
- Answer document-related questions using a custom RAG pipeline powered by Google Gemini.
- Maintain conversation history using Redis.
- Extract interview booking details from natural language using Gemini.
- Interactive API documentation through Swagger UI and ReDoc.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend programming language |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Relational database |
| Qdrant | Vector database |
| Redis | Conversation history management |
| Google Gemini API | LLM-powered question answering and booking extraction |
| Sentence Transformers | Text embedding generation |
| Pydantic | Data validation |

## Project Structure

```text
palm_mind_assignment/
│
├── app/
│   ├── api/
│   │   ├── booking.py
│   │   ├── chat.py
│   │   └── ingestion.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── crud.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   └── booking.py
│   │
│   ├── services/
│   │   ├── chunking_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── qdrant_service.py
│   │   ├── rag_service.py
│   │   └── redis_service.py
│   │
│   └── main.py
│
├── tests/
│   └── test_chunking.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── sample.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ryanxdev01/palm-mind-ai-assignment.git
cd palm-mind-assignment
```

### 2. Create a virtual environment

Python 3.12 is recommended.

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory using `.env.example` as a reference.

Add your credentials:

```env
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6380/0
```

**Important:** Never upload your actual `.env` file or API keys to GitHub.

### 5. Start Redis

Make sure Docker Desktop is running.

Start a Redis container:

```bash
docker run -d --name palm-mind-redis -p 6380:6379 redis
```

If the container already exists, start it using:

```bash
docker start palm-mind-redis
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

Once the application is running, access the following endpoints:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/health

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/ingestion/upload` | Upload and process PDF/TXT documents |
| POST | `/api/v1/chat/ask` | Ask questions about uploaded documents |
| POST | `/api/v1/booking/book` | Book interviews using natural language |

## Database and Storage

- **SQLite:** Stores document metadata and interview booking records.
- **Qdrant:** Stores document embeddings for semantic search.
- **Redis:** Stores conversation history.
- **Local Storage:** Maintains persistent Qdrant data.

## Notes

- A valid Google Gemini API key is required for LLM-powered features.
- Redis must be running before using conversation-related features.
- Qdrant uses local persistent storage.
- The project provides backend APIs and does not include a frontend interface.

## Author

Developed as a technical assignment for a Backend Developer role.

**GitHub Repository:** https://github.com/ryanxdev01/palm-mind-ai-assignment