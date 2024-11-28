from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import get_users_count_2
from Plugins import startTime, grt
from time import time

@Client.on_message(filters.command('users') & filters.user(SUDO_USERS))
async def users(_, m):
    """
    Handles the /users command to display the total number of users.
    """
    count = await get_users_count_2()
    await m.reply(f'Users: {count}.')

@Client.on_message(filters.command('uptime') & filters.user(SUDO_USERS))
async def uptime(_, m):
    """
    Handles the /uptime command to display the bot's uptime.
    """
    uptime_duration = int(time() - startTime)
    formatted_uptime = grt(uptime_duration)
    await m.reply(f'Uptime: {formatted_uptime}.')
