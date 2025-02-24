"""Unit tests for vector service"""

from datetime import datetime as dt
from PIL import Image
import vector_service
import clip_service
from meme import Meme


def test_vectors_are_saved():
    """Tests the vectors are saved"""

    # Arrange
    image = Image.open("./tests/data/meme.jpg")
    vectors = clip_service.get_vectors(image)
    meme = Meme(
        sender="Mr Test",
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id="123",
        channel_id="123",
        message_id="123",
    )

    # Act
    vector_service.upload_vectors(vectors, meme)
    response = vector_service.query_vectors(vectors[0])

    # Assert
    assert response.points[0].score >= 1  # Asserts the vector score is identical
    assert response.points[0].payload == meme.model_dump()

def test_different_memes_are_not_similar():
    """Tests different memes are not flagged as similar"""

    # Arrange
    image_1 = Image.open("./tests/data/monkey_meme_1.jpg")
    image_2 = Image.open("./tests/data/monkey_meme_2.jpg")
    image_3 = Image.open("./tests/data/boomer.jpg")
    image_4 = Image.open("./tests/data/hotdog.png")
    vectors_1 = clip_service.get_vectors(image_1)
    vectors_2 = clip_service.get_vectors(image_2)
    vectors_3 = clip_service.get_vectors(image_3)
    vectors_4 = clip_service.get_vectors(image_4)

    # Act
    vector_service.upload_vectors(vectors_2, Meme(
        sender="Mr Test",
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id="123",
        channel_id="123",
        message_id="123",
    ))
    vector_service.upload_vectors(vectors_3, Meme(
        sender="Mr Test",
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id="123",
        channel_id="123",
        message_id="123",
    ))

    # Assert
    assert vector_service.query_vectors(vectors_1[0]).points == []
    assert vector_service.query_vectors(vectors_4[0]).points == []

def test_similar_memes_are_returned_a_score():
    """Tests similar memes are flagged as similar"""

    # Arrange
    image_1 = Image.open("./tests/data/meme.jpg")
    image_2 = Image.open("./tests/data/croppedmeme.png")
    vectors_1 = clip_service.get_vectors(image_1)
    vectors_2 = clip_service.get_vectors(image_2)

    meme_1 = Meme(
        sender="Mr Test",
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id="123",
        channel_id="123",
        message_id="123",
    )

    # Act
    vector_service.upload_vectors(vectors_1, meme_1)
    response = vector_service.query_vectors(vectors_2[0])

    # Assert
    assert response.points != []
