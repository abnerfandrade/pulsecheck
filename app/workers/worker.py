import json
import asyncio
from datetime import datetime, timezone
from functools import partial
from loguru import logger
from app.services.rabbitmq_producer import rabbit_connection
from app.services.health_check import check_service
from app.services.mongo_client import logs_collection
from app.core.config import settings


def start_worker():
    _, channel = rabbit_connection()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    on_message_callback = partial(worker_callback, loop=loop)

    channel.basic_consume(
        queue=settings.QUEUE_HEALTH_CHECK,
        on_message_callback=on_message_callback,
        auto_ack=True
    )

    logger.info("Worker waiting for messages...")
    channel.start_consuming()


def worker_callback(ch, method, properties, body, loop):
    message = json.loads(body.decode())
    service_id = message["service_id"]
    url = message["url"]

    logger.info(f"Received message: {message}")
    loop.run_until_complete(process_health_check(service_id, url))


async def process_health_check(service_id: int, url: str):
    try:
        result = await check_service(url)

        log_entry = {
            "service_id": service_id,
            "url": url,
            "status": result["status"],
            "success": result["success"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        await logs_collection.insert_one(log_entry)
        logger.info(f"Log registered for {url}: {result['status']}")

    except Exception as e:
        logger.error(f"Error trying to verify service: {str(e)}")


if __name__ == "__main__":
    start_worker()
