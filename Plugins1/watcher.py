from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import add_user_2

# Group ID for processing private messages
watch = 69

@Client.on_message(filters.private, group=watch)
async def cwf(_, m):
    """
    Handles incoming private messages. If the sender is a SUDO user, adds them to the database.
    Otherwise, replies with a predefined message and adds the sender to the database.
    """
    # If the sender is a SUDO user, add them to the database
    if m.from_user and m.from_user.id in SUDO_USERS:
        return await add_user_2(m.from_user.id)
    
    # Reply with a predefined message for non-SUDO users
    await m.reply("**Message Me Here @CuteGirlTG**")
    
    # Add the sender to the database
    await add_user_2(m.from_user.id)
