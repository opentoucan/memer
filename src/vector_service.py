"""Module for persisting vectors to the database"""

from os import environ
from numpy import ndarray
from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse
from qdrant_client.models import Distance, VectorParams
from meme import Meme

vector_client = QdrantClient(
    location=environ.get("QDRANT_URL", ":memory:"),
    api_key=environ.get("QDRANT_API_KEY", None),
)

threshold = environ.get("THRESHOLD", 0.96) is float

if not vector_client.collection_exists(collection_name="memes"):
    vector_client.create_collection(
        collection_name="memes",
        vectors_config={"image": VectorParams(size=512, distance=Distance.COSINE)},
    )


def query_vectors(vectors: ndarray) -> QueryResponse:
    """Retrieves nearest vectors above threshold"""
    return vector_client.query_points(
        collection_name="memes",
        using="image",
        query=vectors,
        score_threshold=threshold,
        limit=50,
    )


def upload_vectors(vectors: ndarray, meme: Meme) -> None:
    """Uploads vectors to database"""
    vector_client.upload_collection(
        collection_name="memes", vectors={"image": vectors}, payload=[meme.model_dump()]
    )
