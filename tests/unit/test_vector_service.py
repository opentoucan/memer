"""Unit tests for vector service"""
from datetime import datetime as dt
from PIL import Image
import vector_service
import clip_service
from meme import Meme

def test_vectors_are_saved():
    """Tests the vectors are saved"""
    # Arrange
    image = Image.open("./tests/data/meme.png")
    vectors = clip_service.get_vectors(image)
    meme = Meme(
        sender="Mr Test",
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id="123",
        channel_id="123",
        message_id="123")

    # Act
    vector_service.upload_vectors(vectors, meme)
    response = vector_service.query_vectors(vectors[0])

    # Assert
    assert response.points[0].score >= 1                    # Asserts the vector score is identical
    assert response.points[0].payload == meme.model_dump()
