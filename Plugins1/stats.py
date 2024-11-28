from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import get_users_count_2
from Plugins import startTime, grt
from time import time

@Client.on_message(filters.command('users') & filters.user(SUDO_USERS))
async def users(client: Client, message: Message):
    """
    Command to get the total count of users.
    """
    count = await get_users_count_2()
    await message.reply(f'Users: {count}.')

@Client.on_message(filters.command('uptime') & filters.user(SUDO_USERS))
async def uptime(client: Client, message: Message):
    """
    Command to get the bot's uptime.
    """
    uptime_duration = int(time() - startTime)
    txt = f'Uptime: {grt(uptime_duration)}.'
    await message.reply(txt)