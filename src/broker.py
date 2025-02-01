import os
from faststream.security import SASLPlaintext
from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    host=os.environ.get("RABBITMQ_HOST", "localhost"),
    port=int(os.environ.get("RABBITMQ_PORT", 5672)),
    security=SASLPlaintext(
        username=os.environ.get("RABBITMQ_USER", "guest"),
        password=os.environ.get("RABBITMQ_PASSWORD", "guest"),
    ),
)
