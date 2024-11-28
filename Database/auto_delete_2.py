from . import db

db = db.auto_delete_2

async def update_2(user_id: int, dic: dict) -> None:
    """
    Update or insert the dictionary for a specific user in the auto_delete_2 collection.
    """
    await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)

async def get_2(user_id: int) -> dict:
    """
    Retrieve the dictionary for a specific user from the auto_delete_2 collection.
    """
    user_data = await db.find_one({'user_id': user_id})
    if user_data:
        return user_data['dic']
    return {}

async def get_all_2() -> list[int]:
    """
    Retrieve a list of all user IDs in the auto_delete_2 collection.
    """
    cursor = db.find()
    user_list = await cursor.to_list(length=None)
    return [user['user_id'] for user in user_list]