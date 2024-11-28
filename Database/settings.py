from . import db

# Accessing the settings collection
db = db.settings

async def update_settings(dic):
    """Update or insert the settings."""
    await db.update_one({'settings': 69}, {'$set': {'actual_settings': dic}}, upsert=True)

async def get_settings():
    """Get the current settings."""
    settings_data = await db.find_one({'settings': 69})
    if settings_data:
        return settings_data['actual_settings']
    return {'auto_approval': False, 'join': False, 'leave': False, 'image': False, 'generate': 10, 'auto_save': False, 'logs': True}
