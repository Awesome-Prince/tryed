from . import db

# Accessing the 'auto_delete_2' collection from the 'db' module
db = db.auto_delete_2  

# Function to update or insert a document for a given user_id in the 'auto_delete_2' collection
async def update_2(user_id, dic):
    await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)

# Function to retrieve the 'dic' field of a user document by user_id from the 'auto_delete_2' collection
async def get_2(user_id):
    x = await db.find_one({'user_id': user_id})
    if x:
        return x['dic']
    return {}  # Return an empty dictionary if no document is found

# Function to fetch all user_ids from the 'auto_delete_2' collection and return them as a list
async def get_all_2() -> list[int]:
    x = db.find()  # Query to get all documents in the collection
    x = await x.to_list(length=None)  # Convert the cursor to a list of documents
    return [y['user_id'] for y in x]  # Extract and return the user_ids as a list
