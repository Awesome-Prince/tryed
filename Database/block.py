from . import db
from config import BOT_TOKEN

# Initialize the database collection for blocked users
db = db[f"block_{BOT_TOKEN.split(':')[0]}"]

async def block(user_id: int) -> None:
    """
    Block a user by inserting their user ID into the block collection.
    """
    await db.insert_one({'user_id': user_id})

async def unblock(user_id: int) -> None:
    """
    Unblock a user by deleting their user ID from the block collection.
    """
    await db.delete_one({'user_id': user_id})

async def is_blocked(user_id: int) -> bool:
    """
    Check if a user is blocked by finding their user ID in the block collection.
    """
    user_data = await db.find_one({'user_id': user_id})
    return bool(user_data)