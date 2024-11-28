from . import db
from config import BOT_TOKEN

# Access the block collection based on BOT_TOKEN
db = db[f"block_{BOT_TOKEN.split(':')[0]}"]

async def block(user_id):
    """Block a user by inserting user_id into the collection."""
    await db.insert_one({'user_id': user_id})

async def unblock(user_id):
    """Unblock a user by deleting user_id from the collection."""
    await db.delete_one({'user_id': user_id})

async def is_blocked(user_id):
    """Check if a user is blocked by searching for user_id in the collection."""
    user_data = await db.find_one({'user_id': user_id})
    return user_data is not None
