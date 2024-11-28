from . import db

# Select the collection for encryption data
db = db.encr

async def update(encr: str, e: str) -> None:
    """
    Update or insert the encryption data for a specific key.
    """
    await db.update_one({"encr": encr}, {"$set": {"e": e}}, upsert=True)

async def get_encr(encr: str) -> str:
    """
    Retrieve the encryption data for a specific key.
    """
    encr_data = await db.find_one({"encr": encr})
    if encr_data:
        return encr_data["e"]
    return None