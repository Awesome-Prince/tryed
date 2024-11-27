from . import db

# Select the collection for count management
db = db.count

# Increment the count by 1 and return the new value
async def incr_count() -> int:
    # Check if the count record exists
    x = await db.find_one({"count": 69})
    if x:
        y = x["actual_count"] + 1  # Increment the count by 1
    else:
        y = 1  # Initialize the count if it doesn't exist
    # Update the count in the database
    await db.update_one({"count": 69}, {"$set": {"actual_count": y}}, upsert=True)
    return y

# Get the current count
async def get_count() -> int:
    # Retrieve the current count value
    x = await db.find_one({"count": 69})
    if x:
        return x["actual_count"]
    return 0  # Return 0 if the count doesn't exist

# Increment the count by a specified value 'c' and return the new value
async def incr_count_by(c: int) -> int:
    # Check if the count record exists
    x = await db.find_one({"count": 69})
    if x:
        y = x["actual_count"] + c  # Increment by the specified value
    else:
        y = c  # Initialize the count with the specified value
    # Update the count in the database
    await db.update_one({"count": 69}, {"$set": {"actual_count": y}}, upsert=True)
    return y

# Reset the count by deleting the count record
async def reset_count():
    # Delete the count record from the database
    await db.delete_one({"count": 69})
