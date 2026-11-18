
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from uuid import uuid4
from qdrant_client.models import PointStruct

# Store Qdrant data locally in this folder
client = QdrantClient(path="./qdrant_data")

COLLECTION_NAME = "documents"


def create_collection() -> None:
    """Create the documents collection if it does not exist."""

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )




def save_document_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str
) -> None:
    """Save document chunks and embeddings in Qdrant."""

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have the same length.")

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "filename": filename,
                    "text": chunk
                }
            )
        )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )


def search_similar_chunks(
    query_embedding: list[float],
    limit: int = 3
) -> list[dict]:
    """Find the most relevant document chunks in Qdrant."""

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True
    )

    results = []

    for point in response.points:
        results.append({
            "score": point.score,
            "filename": point.payload.get("filename"),
            "text": point.payload.get("text")
        })

    return results

