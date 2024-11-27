from . import db
from config import BOT_TOKEN

# Dynamically select the collection based on the bot token (first part before ':')
db = db[f"block_{BOT_TOKEN.split(':')[0]}"]

# Block a user by inserting their user_id into the database
async def block(user_id):
    await db.insert_one({'user_id': user_id})

# Unblock a user by deleting their user_id from the database
async def unblock(user_id):
    await db.delete_one({'user_id': user_id})

# Check if a user is blocked by querying the database for their user_id
async def is_blocked(user_id):
    x = await db.find_one({'user_id': user_id})
    return bool(x)  # Return True if user is blocked, otherwise False
