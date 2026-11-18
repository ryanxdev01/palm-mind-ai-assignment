
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """
    Convert one text into a numerical vector.
    """

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple text chunks into numerical vectors.
    """

    if not texts:
        return []

    embeddings = model.encode(texts)

    return embeddings.tolist()
