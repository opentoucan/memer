"""Module for starting the application"""

import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType
from broker import broker
import meme_posted_event_handler  # noqa: F401


app = FastStream(broker)


async def main():
    """Main function"""
    await app.run()  # blocking method


if __name__ == "__main__":
    asyncio.run(main())


@app.after_startup
async def after_startup():
    """Post startup callback for rabbitmq queue and exchange creation"""
    print("Starting RabbitMQ Exchange")
    meme_posted_queue = await broker.declare_queue(
        RabbitQueue(name="meme-posted-queue", durable=True)
    )
    meme_posted_exchange = await broker.declare_exchange(
        RabbitExchange("meme-posted-exchange", durable=True, type=ExchangeType.TOPIC)
    )
    await broker.declare_exchange(
        RabbitExchange(
            name="meme-repost-exchange",
            durable=True,
            type=ExchangeType.TOPIC,
            routing_key="meme-repost-exchange",
        )
    )
    await meme_posted_queue.bind(
        exchange=meme_posted_exchange,
        routing_key=meme_posted_queue.name,  # Optional parameter
    )
