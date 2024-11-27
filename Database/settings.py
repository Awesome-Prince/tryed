from . import db

# Reference to the settings collection in the database
settings_collection = db.settings

# Default settings dictionary
DEFAULT_SETTINGS = {
    'auto_approval': False,
    'join': False,
    'leave': False,
    'image': False,
    'generate': 10,
    'auto_save': False,
    'logs': True
}

async def update_settings(settings_dict):
    """
    Update the settings in the database.

    Args:
        settings_dict (dict): Dictionary containing the settings to update.
    """
    await settings_collection.update_one(
        {'settings': 69},
        {'$set': {'actual_settings': settings_dict}},
        upsert=True
    )

async def get_settings():
    """
    Retrieve the settings from the database.

    Returns:
        dict: The settings dictionary from the database or the default settings.
    """
    settings = await settings_collection.find_one({'settings': 69})
    if settings:
        return settings.get('actual_settings', DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS