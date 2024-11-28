from . import db

# Accessing the count_2 collection
db = db.count_2

async def incr_count_2() -> int:
    """Increment the count by 1 and return the new count."""
    count_data = await db.find_one({"count_2": 69})
    new_count = (count_data["actual_count_2"] + 1) if count_data else 1
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": new_count}}, upsert=True)
    return new_count

async def get_count_2() -> int:
    """Get the current count value."""
    count_data = await db.find_one({"count_2": 69})
    return count_data["actual_count_2"] if count_data else 0

async def incr_count_2_by(c: int) -> int:
    """Increment the count by a specified value and return the new count."""
    count_data = await db.find_one({"count_2": 69})
    new_count = (count_data["actual_count_2"] + c) if count_data else c
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": new_count}}, upsert=True)
    return new_count

async def reset_count_2():
    """Reset the count by deleting the document."""
    await db.delete_one({"count_2": 69})
