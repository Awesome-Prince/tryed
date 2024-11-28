import asyncio
from pyrogram import Client, filters
from config import SUDO_USERS
from Database.count import reset_count
from Database.count_2 import reset_count_2
from Database import db
from time import time

@Client.on_message(filters.command('reset') & filters.user(SUDO_USERS))
async def reset(client: Client, message: Message):
    """
    Reset the count values in the database.
    """
    await reset_count()
    await reset_count_2()
    await message.reply(' **Count has been reset....** ')

# Variable to confirm the reset of the entire database
confirm = False
t = time()

@Client.on_message(filters.command('resets') & filters.user(SUDO_USERS))
async def resets(client: Client, message: Message):
    """
    Reset the entire database except for count and users collections.
    """
    global confirm, t
    if int(time() - t) > 30:
        confirm = False
    if not confirm:
        confirm = True
        t = time()
        return await message.reply('Are You Sure? You are Doing Reset\nBot Settings if Yes Than Type Again!!..')
    
    collections = await db.list_collection_names()
    for collection_name in collections:
        if 'count' in collection_name or 'users' in collection_name:
            continue
        await db[collection_name].drop()
    
    await message.reply('DB Formatted.')