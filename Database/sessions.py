from . import db

# Accessing the sessions collection
db = db.sessions

async def update_session(user_id, session):
    """Update or insert a session for the given user_id."""
    await db.update_one({'user_id': user_id}, {'$set': {'session': session}}, upsert=True)

async def get_session(user_id):
    """Get the session for the given user_id."""
    user_data = await db.find_one({'user_id': user_id}) or {}
    return user_data.get('session', None)

async def del_session(user_id):
    """Delete the session for the given user_id."""
    await db.delete_one({'user_id': user_id})
