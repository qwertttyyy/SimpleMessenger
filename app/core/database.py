import motor.motor_asyncio

from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
db = client[settings.database_name]
messages_collection = db['messages']
