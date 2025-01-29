from .client import client
from qdrant_client.models import Distance, VectorParams

from ..meme import Meme

if not client.collection_exists(collection_name="memes"):
    client.create_collection(
        collection_name="memes",
        vectors_config={"image": VectorParams(size=512, distance=Distance.COSINE)},
    )

def query_vectors(vectors: []):
    return client.query_points(
        collection_name="memes",
        using="image",
        query=vectors,
        score_threshold=0.95,
        limit=50)

def upload_vectors(vectors: [], meme: Meme):
    client.upload_collection(
        collection_name="memes",
        vectors={"image": vectors},
        payload=[meme])