from . import db

db = db.sessions

# Update the session for a user
async def update_session(user_id, session):
    try:
        await db.update_one({'user_id': user_id}, {'$set': {'session': session}}, upsert=True)
    except Exception as e:
        # Log the error (replace with your logging mechanism)
        print(f"Error updating session for {user_id}: {e}")

# Retrieve the session for a user
async def get_session(user_id):
    try:
        x = await db.find_one({'user_id': user_id}) or {}
        return x.get('session', None)
    except Exception as e:
        # Log the error (replace with your logging mechanism)
        print(f"Error retrieving session for {user_id}: {e}")
        return None

# Delete the session for a user
async def del_session(user_id):
    try:
        await db.delete_one({'user_id': user_id})
    except Exception as e:
        # Log the error (replace with your logging mechanism)
        print(f"Error deleting session for {user_id}: {e}")
