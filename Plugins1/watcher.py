from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import add_user_2

# Watch group to ensure the function runs at the right moment
watch = 69

@Client.on_message(filters.private, group=watch)
async def cwf(_, m):
    """Handle private messages, add users, and respond accordingly."""
    try:
        if m.from_user and m.from_user.id in SUDO_USERS:
            # If the user is a sudo user, add them to the database
            await add_user_2(m.from_user.id)
        else:
            # If the user is not a sudo user, reply with a message
            await m.reply("**Message Me Here @CuteGirlTG**")
            await add_user_2(m.from_user.id)  # Add the user regardless of sudo status
    except Exception as e:
        # Basic error handling to catch potential issues
        print(f"Error in cwf function: {e}")
        await m.reply("Something went wrong while processing your request.")
