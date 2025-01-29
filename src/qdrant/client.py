from os import environ
from qdrant_client import QdrantClient
client = ...
if environ.get("QDRANT_URL") is None:
    client = QdrantClient(":memory:")
else:
    client = QdrantClient(url=environ.get("QDRANT_URL"))


