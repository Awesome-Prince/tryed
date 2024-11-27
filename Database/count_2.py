from . import db

# Select the collection for count_2 management
db = db.count_2

# Increment the count_2 by 1 and return the new value
async def incr_count_2() -> int:
    # Check if the count_2 record exists
    x = await db.find_one({"count_2": 69})
    if x:
        y = x["actual_count_2"] + 1  # Increment the count_2 by 1
    else:
        y = 1  # Initialize the count_2 if it doesn't exist
    # Update the count_2 in the database
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": y}}, upsert=True)
    return y

# Get the current count_2
async def get_count_2() -> int:
    # Retrieve the current count_2 value
    x = await db.find_one({"count_2": 69})
    if x:
        return x["actual_count_2"]
    return 0  # Return 0 if the count_2 doesn't exist

# Increment the count_2 by a specified value 'c' and return the new value
async def incr_count_2_by(c: int) -> int:
    # Check if the count_2 record exists
    x = await db.find_one({"count_2": 69})
    if x:
        y = x["actual_count_2"] + c  # Increment by the specified value
    else:
        y = c  # Initialize the count_2 with the specified value
    # Update the count_2 in the database
    await db.update_one({"count_2": 69}, {"$set": {"actual_count_2": y}}, upsert=True)
    return y

# Reset the count_2 by deleting the count_2 record
async def reset_count_2():
    # Delete the count_2 record from the database
    await db.delete_one({"count_2": 69})
