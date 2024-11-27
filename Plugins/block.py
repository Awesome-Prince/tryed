from config import SUDO_USERS
from pyrogram import Client, filters
from Database.block import *

# Command to block a user
@Client.on_message(filters.command('block') & filters.user(SUDO_USERS))
async def bl(_, m):
    try:
        # Try to get the user ID from the command argument
        id = int(m.text.split()[1])
    except IndexError:
        # If no user ID is provided
        return await m.reply('Usage: /block user_id')
    except ValueError:
        # If the user ID is not a valid integer
        return await m.reply('Please provide a valid user ID.')

    # Check if the user is already blocked
    if await is_blocked(id):
        return await m.reply('**This User is Already Banned.**')

    # Block the user
    await block(id)
    await m.reply(f'**User {id} has been blocked. They can\'t access me now.**')

# Command to unblock a user
@Client.on_message(filters.command('unblock') & filters.user(SUDO_USERS))
async def unbl(_, m):
    try:
        # Try to get the user ID from the command argument
        id = int(m.text.split()[1])
    except IndexError:
        # If no user ID is provided
        return await m.reply('Usage: /unblock user_id')
    except ValueError:
        # If the user ID is not a valid integer
        return await m.reply('Please provide a valid user ID.')

    # Check if the user is not blocked
    if not await is_blocked(id):
        return await m.reply('**This User has access to the bot.**')

    # Unblock the user
    await unblock(id)
    await m.reply(f'**User {id} has been unblocked. They can now use the bot.**')

# Decorator to prevent a blocked user from using the bot
def block_dec(func):
    async def wrapper(_, m):
        if not m.from_user:
            return
        
        # Check if the user is blocked
        if await is_blocked(m.from_user.id):
            # Optionally log the action if needed
            return await m.reply('**You are blocked from using this bot.**')
        
        return await func(_, m)
    return wrapper
