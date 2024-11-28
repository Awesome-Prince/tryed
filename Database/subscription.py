from . import db
import time

# Accessing the subscription collection
db = db.subscription

async def active_sub(user_id):
    """Activate a subscription for the given user_id."""
    await db.update_one({"user_id": user_id}, {"$set": {"time": time.time()}}, upsert=True)

async def get_all_subs():
    """Get all subscriptions."""
    subscriptions = db.find()
    subs_list = await subscriptions.to_list(length=None)
    return {sub["user_id"]: sub["time"] for sub in subs_list}

async def del_sub(user_id):
    """Delete the subscription for the given user_id."""
    await db.delete_one({"user_id": user_id})
