from . import db

# Select the collection for count_2 management
db = db.count_2

async def incr_count_2() -> int:
    """
    Increment the count_2 by 1 and return the new value.
    """
    count_record = await db.find_one({"count_2": 69})
    new_count = count_record["actual_count_2"] + 1 if count_record else 1
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": new_count}}, upsert=True)
    return new_count

async def get_count_2() -> int:
    """
    Retrieve the current count_2 value.
    """
    count_record = await db.find_one({"count_2": 69})
    return count_record["actual_count_2"] if count_record else 0

async def incr_count_2_by(increment: int) -> int:
    """
    Increment the count_2 by a specified value 'increment' and return the new value.
    """
    count_record = await db.find_one({"count_2": 69})
    new_count = count_record["actual_count_2"] + increment if count_record else increment
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": new_count}}, upsert=True)
    return new_count

async def reset_count_2() -> None:
    """
    Reset the count_2 by deleting the count_2 record.
    """
    await db.delete_one({"count_2": 69})