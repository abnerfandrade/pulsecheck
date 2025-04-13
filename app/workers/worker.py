import json
import asyncio
from loguru import logger
from app.services.rabbitmq_producer import rabbit_connection
from app.services.health_check import check_service
from app.services.mongo_client import logs_collection
from app.core.config import settings


def start_worker():
    _, channel = rabbit_connection()

    channel.basic_consume(
        queue=settings.QUEUE_HEALTH_CHECK,
        on_message_callback=worker_callback,
        auto_ack=False
    )

    logger.info("Worker waiting for messages...")
    channel.start_consuming()


def worker_callback(ch, method, properties, body):
    message = json.loads(body.decode())
    service_id = message["service_id"]
    url = message["url"]

    logger.info(f"Received message: {message}")
    asyncio.run(process_health_check(service_id, url))

    ch.basic_ack(delivery_tag=method.delivery_tag)


async def process_health_check(service_id: int, url: str):
    try:
        result = await check_service(url)

        log_entry = {
            "service_id": service_id,
            "url": url,
            "status": result["status"],
            "success": result["success"],
            "timestamp": str(asyncio.get_event_loop().time())
        }

        await logs_collection.insert_one(log_entry)
        logger.info(f"Log registered for {url}: {result['status']}")

    except Exception as e:
        logger.error(f"Error trying to verify service: {str(e)}")


if __name__ == "__main__":
    start_worker()
