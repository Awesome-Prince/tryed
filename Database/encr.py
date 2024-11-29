from . import db

# Accessing the encr collection
db = db.encr

async def update(encr, e):
    """Update or insert encryption data."""
    await db.update_one({"encr": encr}, {"$set": {"e": e}}, upsert=True)

async def get(encr):
    """Get encryption data based on encr value."""
    encr_data = await db.find_one({"encr": encr})
    if encr_data:
        return encr_data["e"]
    return None

async def get_all():
    """Get all encryption data."""
    return await db.find().to_list(None)

def decrypt(text):
    """Decrypt the text."""
    # Add your decryption logic here
    pass

def Char2Int(char):
    """Convert char to int."""
    # Add your char to int conversion logic here
    pass

async def get_encr(encr):
    """Get encrypted data based on encr value."""
    return await get(encr)
