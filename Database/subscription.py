from . import db
import time

db = db.subscription

# Set active subscription for a user
async def active_sub(user_id):
    try:
        await db.update_one({"user_id": user_id}, {"$set": {"time": time.time()}}, upsert=True)
    except Exception as e:
        print(f"Error setting active subscription for user {user_id}: {e}")

# Get all subscriptions and their timestamps
async def get_all_subs():
    try:
        x = db.find()
        x = await x.to_list(length=None)
        # Return dictionary of user_id -> subscription time
        return {u["user_id"]: u["time"] for u in x}
    except Exception as e:
        print(f"Error retrieving subscriptions: {e}")
        return {}

# Delete subscription for a user
async def del_sub(user_id):
    try:
        await db.delete_one({"user_id": user_id})
    except Exception as e:
        print(f"Error deleting subscription for user {user_id}: {e}")
