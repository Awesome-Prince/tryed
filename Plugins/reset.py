from pyrogram import Client, filters
from config import SUDO_USERS
from Database.count import reset_count
from Database.count_2 import reset_count_2
from Database import db
from time import time

@Client.on_message(filters.command('reset') & filters.user(SUDO_USERS))
async def reset(_, m):
    """
    Resets the count values.
    """
    await reset_count()
    await reset_count_2()
    await m.reply('**Count has been reset....**')

confirm_reset = False
last_request_time = time()

@Client.on_message(filters.command('resets') & filters.user(SUDO_USERS))
async def resets(_, m):
    """
    Resets the database, excluding count and users collections.
    This command requires confirmation.
    """
    global confirm_reset, last_request_time
    if int(time() - last_request_time) > 30:
        confirm_reset = False
    if not confirm_reset:
        confirm_reset = True
        last_request_time = time()
        return await m.reply('Are You Sure? You are doing a reset of bot settings.\nIf yes, then type again!!')
    
    collections = await db.list_collection_names()
    for collection_name in collections:
        if 'count' in collection_name or 'users' in collection_name:
            continue
        await db[collection_name].drop()
    
    await m.reply('DB Formatted.')
