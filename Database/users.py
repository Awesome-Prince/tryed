from . import db
from config import BOT_TOKEN, BOT_TOKEN_2

# Initialize the database collections for two different bot tokens
db1 = db[BOT_TOKEN.split(":")[0] + '_users']
db2 = db[BOT_TOKEN_2.split(":")[0] + '_users']

async def add_user_2(user_id: int) -> None:
    """
    Add a user to the second bot's user collection if they don't already exist.
    """
    if await is_user_2(user_id):
        return
    await db2.insert_one({'user_id': user_id})

async def is_user_2(user_id: int) -> bool:
    """
    Check if a user exists in the second bot's user collection.
    """
    user_data = await db2.find_one({'user_id': user_id})
    return bool(user_data)

async def get_users_2() -> list[int]:
    """
    Retrieve a list of user IDs from the second bot's user collection.
    """
    cursor = db2.find()
    user_list = await cursor.to_list(length=None)
    return [user['user_id'] for user in user_list]

async def get_users_count_2() -> int:
    """
    Get the count of users in the second bot's user collection.
    """
    cursor = db2.find()
    return len(await cursor.to_list(length=None))

async def add_user(user_id: int) -> None:
    """
    Add a user to the first bot's user collection if they don't already exist.
    """
    if await is_user(user_id):
        return
    await db1.insert_one({'user_id': user_id})

async def is_user(user_id: int) -> bool:
    """
    Check if a user exists in the first bot's user collection.
    """
    user_data = await db1.find_one({'user_id': user_id})
    return bool(user_data)

async def get_users() -> list[int]:
    """
    Retrieve a list of user IDs from the first bot's user collection.
    """
    cursor = db1.find()
    user_list = await cursor.to_list(length=None)
    return [user['user_id'] for user in user_list]

async def get_users_count() -> int:
    """
    Get the count of users in the first bot's user collection.
    """
    cursor = db1.find()
    return len(await cursor.to_list(length=None))

async def del_user(user_id: int) -> None:
    """
    Delete a user from the first bot's user collection.
    """
    await db1.delete_one({'user_id': user_id})

async def del_user_2(user_id: int) -> None:
    """
    Delete a user from the second bot's user collection.
    """
    await db2.delete_one({'user_id': user_id})