import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.service import Service
from app.services.rabbitmq_producer import publish_message
from app.services.mongo_client import logs_collection
from app.core.database import AsyncSessionLocal


async def dispatcher_loop():
    while True:
        async with AsyncSessionLocal() as session:
            await process_services(session)
        await asyncio.sleep(10)


async def process_services(session: AsyncSession):
    result = await session.execute(select(Service))
    services = result.scalars().all()

    for service in services:
        should_send = await should_send_health_check(service)
        if should_send:
            publish_message({"service_id": service.id, "url": service.url})


async def should_send_health_check(service: Service) -> bool:
    last_log = await logs_collection.find_one(
        {"service_id": service.id},
        sort=[("created_at", -1)]
    )

    if not last_log:
        return True

    now = datetime.now(timezone.utc)
    last_check_time = datetime.fromisoformat(last_log["created_at"])
    frequency = getattr(service, "frequency", 60)

    if now >= last_check_time + timedelta(seconds=frequency):
        return True

    return False


if __name__ == "__main__":
    asyncio.run(dispatcher_loop())
