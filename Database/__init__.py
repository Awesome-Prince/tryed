from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

# Initialize MongoDB client
mongo = AsyncIOMotorClient(MONGO_DB_URI)

# Access specific database
db = mongo.SpL
