from . import db

db = db.settings

# Update settings with the given dictionary
async def update_settings(dic):
    try:
        await db.update_one({'settings': 69}, {'$set': {'actual_settings': dic}}, upsert=True)
    except Exception as e:
        # Log the error (replace with your logging mechanism)
        print(f"Error updating settings: {e}")

# Get current settings
async def get_settings():
    try:
        x = await db.find_one({'settings': 69})
        if x:
            return x['actual_settings']
        # Default settings if no record is found
        return {'auto_approval': False, 'join': False, 'leave': False, 'image': False, 
                'generate': 10, 'auto_save': False, 'logs': True}
    except Exception as e:
        # Log the error (replace with your logging mechanism)
        print(f"Error retrieving settings: {e}")
        # Return default settings if error occurs
        return {'auto_approval': False, 'join': False, 'leave': False, 'image': False, 
                'generate': 10, 'auto_save': False, 'logs': True}
