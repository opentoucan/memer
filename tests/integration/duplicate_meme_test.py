import io
import pytest
import base64

from PIL import Image
from faststream import Logger

from src import clip_service
from src.meme_posted_event import MemePosted
from src.qdrant import meme_service
from src.main import handler, broker

from faststream.rabbit import TestRabbitBroker

@broker.subscriber("meme-posted-queue", exchange="meme-posted-exchange")
async def handler(logger: Logger, body: str):
    logger.info(f"Received meme-posted-event: {body}")

@pytest.mark.asyncio
async def test_new_meme_is_saved():
    async with TestRabbitBroker(broker) as br:
        avatar_byte_arr = io.BytesIO()
        meme_byte_arr = io.BytesIO()
        avatar = Image.open("../resources/test_data/avatar.png")
        meme = Image.open("../resources/test_data/meme.png")
        avatar.save(avatar_byte_arr, format=avatar.format)
        meme.save(meme_byte_arr, format=meme.format)

        meme_posted = MemePosted(sender="De Moai", avatar=base64.b64encode(avatar_byte_arr.getvalue()),
                                 meme=base64.b64encode(meme_byte_arr.getvalue()), guild_id="123456789",
                                 channel_id="123456789", message_id="123456789", name_colour="#000000")
        await br.publish(meme_posted.model_dump_json(), exchange="meme-posted-exchange")

    vectors = clip_service.get_vectors(meme)
    points = meme_service.query_vectors(vectors[0])
    handler.mock.assert_called_once_with(meme_posted.model_dump_json())
    assert handler.mock is None
    assert vectors is not None
    assert len(points.points) > 0