from . import db

# Accessing the privileges collection
db = db.privileges

async def update_privileges(user_id, allow_batch, super_user, my_content, allow_dm):
    """Update or insert user privileges."""
    await db.update_one(
        {"user_id": user_id},
        {"$set": {"privileges": [allow_batch, super_user, my_content, allow_dm]}},
        upsert=True
    )

async def get_privileges(user_id):
    """Get user privileges based on user_id."""
    user_data = await db.find_one({"user_id": user_id})
    if user_data:
        return user_data["privileges"]
    return [False, False, False, False]
