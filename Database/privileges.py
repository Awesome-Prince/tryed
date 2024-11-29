from . import db
import logging

# Accessing the privileges collection
db = db.privileges

async def update_privileges(user_id, allow_batch, super_user, my_content, allow_dm):
    """Update or insert user privileges."""
    try:
        result = await db.update_one(
            {"user_id": user_id},
            {"$set": {"privileges": [allow_batch, super_user, my_content, allow_dm]}},
            upsert=True
        )
        if result.upserted_id:
            logging.info(f"Privileges inserted for user {user_id}.")
        else:
            logging.info(f"Privileges updated for user {user_id}.")
    except Exception as e:
        logging.error(f"Error updating privileges for user {user_id}: {e}")

async def get_privileges(user_id):
    """Get user privileges based on user_id."""
    try:
        user_data = await db.find_one({"user_id": user_id})
        if user_data:
            return user_data["privileges"]
        logging.warning(f"No privileges found for user {user_id}, returning default.")
        return [False, False, False, False]
    except Exception as e:
        logging.error(f"Error retrieving privileges for user {user_id}: {e}")
        return [False, False, False, False]
