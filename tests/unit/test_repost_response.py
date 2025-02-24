"""Unit tests for the repost response"""

from datetime import datetime as dt
from PIL import Image
import repost_response


def test_repost_response_is_not_null():
    """Tests the repost response image is not null"""

    response = repost_response.generate_image(
        username="Mr Test",
        colour="#EEEEEE",
        timestamp=dt.now(),
        avatar=Image.open("./tests/data/avatar.png"),
        meme=Image.open("./tests/data/meme.jpg"),
    )

    assert response is not None
