from . import db

# Select the collection for managing user sessions
db = db.sessions

async def update_session(user_id: int, session: str) -> None:
    """
    Update or insert the session for a specific user.
    """
    await db.update_one({'user_id': user_id}, {'$set': {'session': session}}, upsert=True)

async def get_session(user_id: int) -> str:
    """
    Retrieve the session for a specific user.
    """
    user_data = await db.find_one({'user_id': user_id}) or {}
    return user_data.get('session', None)

async def del_session(user_id: int) -> None:
    """
    Delete the session for a specific user.
    """
    await db.delete_one({'user_id': user_id})