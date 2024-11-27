from . import db

db = db.privileges

async def update_privileges(user_id: int, allow_batch: bool, super_user: bool, my_content: bool, allow_dm: bool) -> None:
    """
    Update or insert the privileges for a specific user.
    """
    privileges = [allow_batch, super_user, my_content, allow_dm]
    await db.update_one({"user_id": user_id}, {"$set": {"privileges": privileges}}, upsert=True)

async def get_privileges(user_id: int) -> list:
    """
    Retrieve the privileges for a specific user.
    """
    user_data = await db.find_one({"user_id": user_id})
    if user_data:
        return user_data["privileges"]
    return [False, False, False, False]