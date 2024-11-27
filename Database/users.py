from . import db
from config import BOT_TOKEN, BOT_TOKEN_2

db1 = db[BOT_TOKEN.split(":")[0] + '_users']
db2 = db[BOT_TOKEN_2.split(":")[0] + '_users']

# Helper function to handle user operations for both dbs
async def add_user_to_db(db, user_id):
    try:
        if await is_user_in_db(db, user_id):
            return
        await db.insert_one({'user_id': user_id})
    except Exception as e:
        print(f"Error adding user {user_id} to the database: {e}")

async def is_user_in_db(db, user_id) -> bool:
    try:
        x = await db.find_one({'user_id': user_id})
        return bool(x)
    except Exception as e:
        print(f"Error checking if user {user_id} exists in the database: {e}")
        return False

async def get_users_from_db(db) -> list[int]:
    try:
        x = db.find()
        x = await x.to_list(length=None)
        return [y['user_id'] for y in x]
    except Exception as e:
        print(f"Error retrieving users from the database: {e}")
        return []

async def get_users_count_from_db(db) -> int:
    try:
        return await db.count_documents({})
    except Exception as e:
        print(f"Error counting users in the database: {e}")
        return 0

async def del_user_from_db(db, user_id: int) -> None:
    try:
        await db.delete_one({'user_id': user_id})
    except Exception as e:
        print(f"Error deleting user {user_id} from the database: {e}")

# For Bot 1
async def add_user(user_id):
    await add_user_to_db(db1, user_id)

async def is_user(user_id) -> bool:
    return await is_user_in_db(db1, user_id)

async def get_users() -> list[int]:
    return await get_users_from_db(db1)

async def get_users_count() -> int:
    return await get_users_count_from_db(db1)

async def del_user(user_id: int) -> None:
    await del_user_from_db(db1, user_id)

# For Bot 2
async def add_user_2(user_id):
    await add_user_to_db(db2, user_id)

async def is_user_2(user_id) -> bool:
    return await is_user_in_db(db2, user_id)

async def get_users_2() -> list[int]:
    return await get_users_from_db(db2)

async def get_users_count_2() -> int:
    return await get_users_count_from_db(db2)

async def del_user_2(user_id: int) -> None:
    await del_user_from_db(db2, user_id)
