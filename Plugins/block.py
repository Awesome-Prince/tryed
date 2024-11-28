from config import SUDO_USERS
from pyrogram import Client, filters
from Database.block import *

@Client.on_message(filters.command('block') & filters.user(SUDO_USERS))
async def bl(client: Client, message: Message):
    """
    Command to block a user by their user ID.
    """
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        return await message.reply('Usage: /block user_id')
    
    if await is_blocked(user_id):
        return await message.reply('**This User is Already BANNED.**')
    
    await block(user_id)
    await message.reply('**This User Can\'t Access Me Now ...**')

@Client.on_message(filters.command('unblock') & filters.user(SUDO_USERS))
async def unbl(client: Client, message: Message):
    """
    Command to unblock a user by their user ID.
    """
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        return await message.reply('Usage: /unblock user_id')
    
    if not await is_blocked(user_id):
        return await message.reply('**This User Already Has My Access...**')
    
    await unblock(user_id)
    await message.reply('**This User Can Use BOT Now ...**')

def block_dec(func):
    """
    Decorator to check if a user is blocked before processing the message.
    """
    async def wrapper(client: Client, message: Message):
        if not message.from_user:
            return
        if await is_blocked(message.from_user.id):
            return
        return await func(client, message)
    
    return wrapper