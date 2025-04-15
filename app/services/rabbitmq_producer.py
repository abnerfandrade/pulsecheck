import json
import pika
from loguru import logger
from app.core.config import settings


def rabbit_connection() -> pika.BlockingConnection:
    connection = pika.BlockingConnection(
        pika.URLParameters(settings.RABBITMQ_URL)
    )
    channel = connection.channel()

    channel.queue_declare(queue=settings.QUEUE_HEALTH_CHECK)

    return connection, channel


def publish_message(message: dict):
    connection, channel = rabbit_connection()

    queue = settings.QUEUE_HEALTH_CHECK
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message)
    )

    logger.info(f"Message sent to queue {queue} with payload: {message}")
    connection.close()
