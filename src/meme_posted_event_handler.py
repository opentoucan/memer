"""Module for handling"""
import base64
import io
import json
from io import BytesIO
from datetime import datetime as dt
from faststream import Logger
from PIL import Image
from pydantic.v1.json import pydantic_encoder
import clip_service
import repost_response
import vector_service
from main import broker
from meme import Meme
from meme_posted_event import MemePosted
from repost_event import RepostEvent, Link

@broker.subscriber("meme-posted-queue")
async def handle(logger: Logger, body: str):
    """Handle method for meme posted events"""
    logger.info(f"Received meme-posted-event: {body}")
    meme_posted = MemePosted(**json.loads(body))
    avatar: Image.Image = Image.open(BytesIO(base64.b64decode(meme_posted.avatar)))
    meme_image: Image.Image = Image.open(BytesIO(base64.b64decode(meme_posted.meme)))

    vectors = clip_service.get_vectors(meme_image)
    points = vector_service.query_vectors(vectors[0])

    repost_meme_links = []
    for point in points.points:
        duplicate_meme = Meme(**json.loads(point.model_dump_json()))
        repost_meme_links.append(Link(
            guild_id=duplicate_meme.guild_id,
            channel_id=duplicate_meme.channel_id,
            message_id=duplicate_meme.message_id))

    meme = Meme(
        sender=meme_posted.sender,
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id=meme_posted.guild_id,
        channel_id=meme_posted.channel_id,
        message_id=meme_posted.message_id)

    vector_service.upload_vectors(vectors[0], meme)

    if len(repost_meme_links) <= 0:
        print("No duplicate memes found")
        return

    template = repost_response.generate_image(
                        username=meme_posted.sender,
                        colour=meme_posted.name_colour,
                        timestamp=dt.now(),
                        avatar=avatar,
                        meme=meme_image)

    image_bytes = io.BytesIO()
    template.save(image_bytes)

    repose_event = RepostEvent(
        channel_id=meme_posted.channel_id,
        reply_image=image_bytes.getvalue(),
        links=repost_meme_links)

    message = json.dumps(repose_event, default=pydantic_encoder)
    # Fan out exchange so the routing key shouldn't be used
    await broker.publish(message, exchange="repost-exchange")
