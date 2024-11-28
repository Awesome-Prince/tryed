from . import db

# Accessing the paid collection
db = db.paid

async def pay(user_id):
    """Mark a user as paid by inserting user_id into the collection."""
    await db.insert_one({'user_id': user_id})

async def unpay(user_id):
    """Unmark a user as paid by deleting user_id from the collection."""
    await db.delete_one({'user_id': user_id})

async def is_paid(user_id):
    """Check if a user is marked as paid."""
    user_data = await db.find_one({'user_id': user_id})
    return user_data is not None
