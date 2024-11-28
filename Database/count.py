from . import db

# Accessing the count collection
db = db.count

async def incr_count() -> int:
    """Increment the count by 1 and return the new count."""
    count_data = await db.find_one({"count": 69})
    new_count = (count_data["actual_count"] + 1) if count_data else 1
    await db.update_one({"count": 69}, {"$set": {"actual_count": new_count}}, upsert=True)
    return new_count

async def get_count() -> int:
    """Get the current count value."""
    count_data = await db.find_one({"count": 69})
    return count_data["actual_count"] if count_data else 0

async def incr_count_by(c: int) -> int:
    """Increment the count by a specified value and return the new count."""
    count_data = await db.find_one({"count": 69})
    new_count = (count_data["actual_count"] + c) if count_data else c
    await db.update_one({"count": 69}, {"$set": {"actual_count": new_count}}, upsert=True)
    return new_count

async def reset_count():
    """Reset the count by deleting the document."""
    await db.delete_one({"count": 69})
