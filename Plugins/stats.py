from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import get_users_count
from . import startTime, grt
from time import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command('users') & filters.user(SUDO_USERS))
async def users(_, m):
    try:
        # Get the count of users from the database
        count = await get_users_count()
        await m.reply(f'Users: {count}.')
        logging.info(f'Users count sent to {m.from_user.id}. Total users: {count}')
    except Exception as e:
        logging.error(f"Error fetching user count: {e}")
        await m.reply('Sorry, there was an error fetching the user count.')

@Client.on_message(filters.command('uptime') & filters.user(SUDO_USERS))
async def uptime(_, m):
    try:
        # Calculate the uptime
        uptime_text = 'Uptime: {}.'
        uptime_text = uptime_text.format(grt(int(time() - startTime)))
        await m.reply(uptime_text)
        logging.info(f'Uptime sent to {m.from_user.id}: {uptime_text}')
    except Exception as e:
        logging.error(f"Error fetching uptime: {e}")
        await m.reply('Sorry, there was an error fetching the uptime.')
