from . import db

# Select the collection for count management
db = db.count

async def incr_count() -> int:
    """
    Increment the count by 1 and return the new value.
    """
    count_record = await db.find_one({"count": 69})
    new_count = count_record["actual_count"] + 1 if count_record else 1
    await db.update_one({"count": 69}, {"$set": {"actual_count": new_count}}, upsert=True)
    return new_count

async def get_count() -> int:
    """
    Retrieve the current count value.
    """
    count_record = await db.find_one({"count": 69})
    return count_record["actual_count"] if count_record else 0

async def incr_count_by(increment: int) -> int:
    """
    Increment the count by a specified value 'increment' and return the new value.
    """
    count_record = await db.find_one({"count": 69})
    new_count = count_record["actual_count"] + increment if count_record else increment
    await db.update_one({"count": 69}, {"$set": {"actual_count": new_count}}, upsert=True)
    return new_count

async def reset_count() -> None:
    """
    Reset the count by deleting the count record.
    """
    await db.delete_one({"count": 69})