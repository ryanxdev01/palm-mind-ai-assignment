
from typing import Literal

from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.crud import create_document_metadata
from app.services.qdrant_service import create_collection, save_document_chunks
from app.services.document_service import extract_document_text
from app.services.embedding_service import generate_embeddings
from app.services.chunking_service import (
    fixed_size_chunking,
    recursive_character_chunking
)

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: Literal["fixed", "recursive"] = Query(
        default="fixed",
        description="Choose fixed or recursive chunking."
    ),
    db: Session = Depends(get_db)
):

    # Check whether a filename was provided
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    # Check file extension
    file_extension = "." + file.filename.rsplit(".", 1)[-1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed."
        )

    # Read the uploaded file
    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB."
        )

    # Validate PDF or TXT content
    if file_extension == ".pdf":
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file."
            )

    elif file_extension == ".txt":
        try:
            content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="TXT file must use UTF-8 encoding."
            )

    # Extract text
    try:
        extracted_text = extract_document_text(
            content,
            file_extension
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    # Apply selected chunking strategy
    if chunking_strategy == "fixed":
        chunks = fixed_size_chunking(
            extracted_text,
            chunk_size=500,
            overlap=50
        )

    else:
        chunks = recursive_character_chunking(
            extracted_text,
            chunk_size=500,
            overlap=50
        )

    # Generate embeddings for all document chunks
    embeddings = generate_embeddings(chunks)

    # Save chunks and embeddings in Qdrant
    create_collection()

    save_document_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename
    )

    document = create_document_metadata(
    db=db,
    filename=file.filename,
    file_type=file_extension,
    size_bytes=len(content),
    character_count=len(extracted_text),
    chunking_strategy=chunking_strategy,
    total_chunks=len(chunks)
    )

    # Return extracted text and chunks
    return {
        "message": "Document uploaded and processed successfully.",
        "filename": file.filename,
        "file_type": file_extension,
        "size_bytes": len(content),
        "character_count": len(extracted_text),
        "chunking_strategy": chunking_strategy,
        "total_chunks": len(chunks),
        "text_preview": extracted_text[:300],
        "embedding_dimensions": 384,
        "total_embeddings": len(embeddings),
        "document_id": document.id,
        "document_id": document.id,
        "database_message": "Document metadata saved successfully.",
    }
