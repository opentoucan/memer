"""Module for starting the application"""
import os
import asyncio
from faststream import FastStream
from faststream.security import SASLPlaintext
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange

broker = RabbitBroker(
    host=os.environ.get('RABBITMQ_HOST', "localhost"),
    port=int(os.environ.get('RABBITMQ_PORT', 5672)),
    security=SASLPlaintext(username=os.environ.get('RABBITMQ_USER', 'guest'),
                           password=os.environ.get('RABBITMQ_PASSWORD', 'guest')))

app = FastStream(broker)

async def main():
    """Main function"""
    await app.run()  # blocking method

if __name__ == "__main__":
    asyncio.run(main())

@app.after_startup
async def after_startup():
    """Post startup callback for rabbitmq queue and exchange creation"""
    await broker.declare_queue(RabbitQueue(name="meme-posted-queue", durable=True))
    await broker.declare_exchange(RabbitExchange(name="repost-exchange", durable=True))
