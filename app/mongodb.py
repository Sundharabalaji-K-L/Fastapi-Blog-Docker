from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient('mongodb://localhost:27017/')
database = client['blog']
