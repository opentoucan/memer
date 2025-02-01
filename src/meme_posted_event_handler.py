"""Module for handling"""

import base64
import io
import json
from io import BytesIO
from datetime import datetime as dt
from faststream import Logger
from faststream.rabbit import RabbitQueue
from faststream.rabbit import RabbitExchange
from faststream.rabbit import ExchangeType

from PIL import Image
import clip_service
import repost_response
import vector_service
from broker import broker
from meme import Meme
from meme_posted_event import MemePosted
from repost_event import RepostEvent, Link


@broker.subscriber(
    RabbitQueue(name="meme-posted-queue", durable=True),
    exchange=RabbitExchange(
        "meme-posted-exchange", durable=True, type=ExchangeType.TOPIC
    ),
)
async def handle(logger: Logger, body: str):
    """Handle method for meme posted events"""
    meme_posted = MemePosted(**json.loads(body))
    logger.info(
        f"Received meme-posted-event:{meme_posted.model_dump_json(exclude={'meme', 'avatar'})}"
    )
    avatar: Image.Image = Image.open(BytesIO(base64.b64decode(meme_posted.avatar)))
    meme_image: Image.Image = Image.open(BytesIO(base64.b64decode(meme_posted.meme)))

    vectors = clip_service.get_vectors(meme_image)
    points = vector_service.query_vectors(vectors[0])

    repost_meme_links = []
    for point in points.points:
        point_model = point.model_dump()

        print(point_model["payload"])

        repost_meme_links.append(
            Link(
                guild_id=point_model["payload"]["guild_id"],
                channel_id=point_model["payload"]["channel_id"],
                message_id=point_model["payload"]["message_id"],
                score=point_model["score"],
            )
        )

    meme = Meme(
        sender=meme_posted.sender,
        timestamp=dt.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        guild_id=meme_posted.guild_id,
        channel_id=meme_posted.channel_id,
        message_id=meme_posted.message_id,
    )

    vector_service.upload_vectors(vectors, meme)

    if len(repost_meme_links) <= 0:
        print("No duplicate memes found")
        return

    template = repost_response.generate_image(
        username=meme_posted.sender,
        colour=meme_posted.name_colour,
        timestamp=dt.now(),
        avatar=avatar,
        meme=meme_image,
    )

    image_bytes = io.BytesIO()
    template.save(image_bytes, format=template.format)
    repost_event = RepostEvent(
        channel_id=meme_posted.channel_id,
        guild_id=meme_posted.guild_id,
        reply_image=base64.b64encode(image_bytes.getvalue()),
        links=repost_meme_links,
    )

    # Fan out exchange so the routing key shouldn't be used
    await broker.publish(
        repost_event.model_dump_json(),
        exchange=RabbitExchange(
            name="meme-repost-exchange", durable=True, type=ExchangeType.TOPIC
        ),
        routing_key="meme-repost-exchange",
    )
