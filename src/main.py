from faststream import FastStream
import os
import base64
import json
import asyncio

from io import BytesIO
from datetime import datetime as dt
from PIL import Image
from pydantic.v1.json import pydantic_encoder
from faststream.security import SASLPlaintext
from faststream import Logger
from faststream.rabbit import RabbitBroker

from src import clip_service, template_builder
from src.repost_event import RepostEvent, Link
from src.meme_posted_event import MemePosted
from src.meme import Meme
from src.qdrant import meme_service

broker = RabbitBroker(
    host=os.environ.get('RABBITMQ_HOST', "localhost"),
    port=os.environ.get('RABBITMQ_PORT', 5672),
    security=SASLPlaintext(username=os.environ.get('RABBITMQ_USER', 'guest'),
                           password=os.environ.get('RABBITMQ_PASSWORD', 'guest')))

app = FastStream(broker)

async def main():
    await app.run()  # blocking method

if __name__ == "__main__":
    asyncio.run(main())

@broker.subscriber("meme-posted-queue", exchange="meme-posted-exchange")
async def handler(logger: Logger, body: str):
    logger.info(f"Received meme-posted-event: {body}")
    meme_posted = MemePosted(**json.loads(body))
    avatar = Image.open(BytesIO(base64.b64decode(meme_posted.avatar)))
    meme_image = Image.open(BytesIO(base64.b64decode(meme_posted.meme)))

    vectors = clip_service.get_vectors(meme_image)
    points = meme_service.query_vectors(vectors[0])
    repost_meme_links = []
    for point in points.points:
        duplicate_meme = Meme(**json.loads(point.json()))
        repost_meme_links.append(Link(guild_id=duplicate_meme.guild_id, channel_id=duplicate_meme.channel_id,
                                         message_id=duplicate_meme.message_id))

    meme_service.upload_vectors(vectors[0],
                                Meme(meme_posted.sender, dt.now(), meme_posted.guild_id, meme_posted.channel_id, meme_posted.message_id))

    if len(repost_meme_links) <= 0:
        print("No duplicate memes found")
        return

    repose_event = RepostEvent(channel_id=meme_posted.channel_id,
                reply_image=template_builder.build_template(
                        meme_posted.sender,
                        meme_posted.name_colour,
                        dt.now(),
                        avatar,
                        meme_image),
                links=repost_meme_links)

    message = json.dumps(repose_event, default=pydantic_encoder)
    #Fan out exchange so the routing key shouldn't be used
    await broker.publish(message, exchange="repost-exchange")