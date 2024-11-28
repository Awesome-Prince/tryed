from . import db

# Accessing the auto_delete_2 collection
db = db.auto_delete_2

async def update_2(user_id, dic):
    """Update or insert user data based on user_id."""
    await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)

async def get_2(user_id):
    """Get user data based on user_id."""
    user_data = await db.find_one({'user_id': user_id})
    if user_data:
        return user_data.get('dic', {})
    return {}

async def get_all_2() -> list[int]:
    """Get all user_ids from the collection."""
    all_users = db.find()
    all_users_list = await all_users.to_list(length=None)
    return [user['user_id'] for user in all_users_list]
