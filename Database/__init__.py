from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

# Initialize the MongoDB client
mongo = AsyncIOMotorClient(MONGO_DB_URI)

# Select the database
db = mongo.SpL