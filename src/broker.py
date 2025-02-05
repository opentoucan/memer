import os
from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    url=os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
)
