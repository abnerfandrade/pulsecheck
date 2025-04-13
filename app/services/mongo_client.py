from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

motor_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = motor_client.pulsecheck_db
logs_collection = mongo_db.service_logs
