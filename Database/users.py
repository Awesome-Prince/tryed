from . import db
from config import BOT_TOKEN, BOT_TOKEN_2

# Accessing the user collections based on BOT_TOKEN and BOT_TOKEN_2
db1 = db[BOT_TOKEN.split(":")[0] + '_users']
db2 = db[BOT_TOKEN_2.split(":")[0] + '_users']

async def add_user_2(user_id):
    """Add a user to the second user collection if not already present."""
    if await is_user_2(user_id):
        return
    await db2.insert_one({'user_id': user_id})

async def is_user_2(user_id) -> bool:
    """Check if a user exists in the second user collection."""
    user_data = await db2.find_one({'user_id': user_id})
    return user_data is not None

async def get_users_2() -> list[int]:
    """Get all user IDs from the second user collection."""
    users = db2.find()
    users_list = await users.to_list(length=None)
    return [user['user_id'] for user in users_list]

async def get_users_count_2() -> int:
    """Get the count of users in the second user collection."""
    users = db2.find()
    return len(await users.to_list(length=None))

async def add_user(user_id):
    """Add a user to the first user collection if not already present."""
    if await is_user(user_id):
        return
    await db1.insert_one({'user_id': user_id})

async def is_user(user_id) -> bool:
    """Check if a user exists in the first user collection."""
    user_data = await db1.find_one({'user_id': user_id})
    return user_data is not None

async def get_users() -> list[int]:
    """Get all user IDs from the first user collection."""
    users = db1.find()
    users_list = await users.to_list(length=None)
    return [user['user_id'] for user in users_list]

async def get_users_count() -> int:
    """Get the count of users in the first user collection."""
    users = db1.find()
    return len(await users.to_list(length=None))

async def del_user(user_id: int) -> None:
    """Delete a user from the first user collection."""
    await db1.delete_one({'user_id': user_id})

async def del_user_2(user_id: int) -> None:
    """Delete a user from the second user collection."""
    await db2.delete_one({'user_id': user_id})
