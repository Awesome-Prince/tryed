from . import db

db = db.auto_delete

async def update(user_id: int, dic: dict) -> None:
    """
    Update or insert the dictionary for a specific user.
    """
    await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)

async def get(user_id: int) -> dict:
    """
    Retrieve the dictionary for a specific user.
    """
    user_data = await db.find_one({'user_id': user_id})
    if user_data:
        return user_data['dic']
    return {}

async def get_all() -> list[int]:
    """
    Retrieve a list of all user IDs in the auto_delete collection.
    """
    cursor = db.find()
    user_list = await cursor.to_list(length=None)
    return [user['user_id'] for user in user_list]