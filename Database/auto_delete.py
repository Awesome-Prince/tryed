from . import db

db = db.auto_delete  # Access the 'auto_delete' collection from the 'db' module

# Function to update or insert a document for a given user_id
async def update(user_id, dic):
    try:
        await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)
    except Exception as e:
        print(f"Error in update: {e}")

# Function to retrieve the 'dic' field of a user document by user_id
async def get(user_id):
    try:
        x = await db.find_one({'user_id': user_id})
        if x:
            return x['dic']
    except Exception as e:
        print(f"Error in get: {e}")
    return {}  # Return an empty dictionary if no document is found

# Function to fetch all user_ids from the collection and return them as a list
async def get_all() -> list[int]:
    try:
        x = await db.find()  # Query to get all documents in the collection
        x = await x.to_list(length=None)  # Convert the cursor to a list of documents
        return [y['user_id'] for y in x]  # Extract and return the user_ids as a list
    except Exception as e:
        print(f"Error in get_all: {e}")
    return []  # Return an empty list in case of error
