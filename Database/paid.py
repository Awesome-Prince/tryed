from . import db

# Select the collection for managing paid users
db = db.paid

async def pay(user_id: int) -> None:
    """
    Mark a user as paid by inserting their user ID into the paid collection.
    """
    await db.insert_one({'user_id': user_id})

async def unpay(user_id: int) -> None:
    """
    Unmark a user as paid by deleting their user ID from the paid collection.
    """
    await db.delete_one({'user_id': user_id})

async def is_paid(user_id: int) -> bool:
    """
    Check if a user is marked as paid by finding their user ID in the paid collection.
    """
    user_data = await db.find_one({'user_id': user_id})
    return bool(user_data)