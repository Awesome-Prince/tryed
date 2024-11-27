from . import db

# Reference to the auto_delete collection in the database
auto_delete_collection = db.auto_delete

async def update(user_id: int, settings_dict: dict):
    """
    Update the auto-delete settings for a specific user.

    Args:
        user_id (int): The user's ID.
        settings_dict (dict): Dictionary containing the settings to update.
    """
    await auto_delete_collection.update_one(
        {'user_id': user_id},
        {'$set': {'settings': settings_dict}},
        upsert=True
    )

async def get(user_id: int) -> dict:
    """
    Retrieve the auto-delete settings for a specific user.

    Args:
        user_id (int): The user's ID.

    Returns:
        dict: The user's auto-delete settings or an empty dictionary if not found.
    """
    user_settings = await auto_delete_collection.find_one({'user_id': user_id})
    if user_settings:
        return user_settings.get('settings', {})
    return {}

async def get_all() -> list[int]:
    """
    Retrieve all user IDs from the auto-delete collection.

    Returns:
        list[int]: A list of user IDs.
    """
    users_cursor = auto_delete_collection.find()
    users_list = await users_cursor.to_list(length=None)
    return [user['user_id'] for user in users_list]