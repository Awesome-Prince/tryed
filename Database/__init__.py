from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

# Create an AsyncIOMotorClient instance with the MongoDB URI from the config
mongo = AsyncIOMotorClient(MONGO_DB_URI)

# Access the 'SpL' database from the MongoDB client
db = mongo.SpL
