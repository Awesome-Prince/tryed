from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import get_users_count_2
from Plugins import startTime, grt
from time import time

@Client.on_message(filters.command('users') & filters.user(SUDO_USERS))
async def users(_, m):
    """Fetch and respond with the total number of users."""
    try:
        count = await get_users_count_2()  # Get the user count from the database
        await m.reply(f'Users: {count}.')  # Reply with the user count
    except Exception as e:
        await m.reply(f"Error fetching user count: {e}")

@Client.on_message(filters.command('uptime') & filters.user(SUDO_USERS))
async def uptime(_, m):
    """Respond with the bot's uptime since the start."""
    try:
        # Calculate the uptime and format it using 'grt'
        uptime_duration = grt(int(time() - startTime))
        await m.reply(f'Uptime: {uptime_duration}.')  # Reply with the formatted uptime
    except Exception as e:
        await m.reply(f"Error fetching uptime: {e}")
