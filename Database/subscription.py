from . import db
import time

# Select the collection for managing subscriptions
db = db.subscription

async def active_sub(user_id: int) -> None:
    """
    Activate a subscription by updating or inserting the user ID with the current time.
    """
    await db.update_one({"user_id": user_id}, {"$set": {"time": time.time()}}, upsert=True)

async def get_all_subs() -> dict[int, float]:
    """
    Retrieve all subscriptions as a dictionary with user IDs and their subscription times.
    """
    cursor = db.find()
    subs_list = await cursor.to_list(length=None)
    return {user["user_id"]: user["time"] for user in subs_list}

async def del_sub(user_id: int) -> None:
    """
    Delete a subscription by removing the user ID from the subscription collection.
    """
    await db.delete_one({"user_id": user_id})