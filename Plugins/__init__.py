from time import time
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import TUTORIAL_LINK, AUTO_DELETE_TIME
from .start import build

# Helper function to handle rate limits
async def tryer(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)

# Converts seconds into a human-readable format (S, M, H)
def format_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}S"
    if seconds < 3600:
        return f"{int(seconds / 60)}M"
    return f"{int(seconds / 3600)}H"

# Returns a shorter time format for seconds (S, M, 60M+)
def format_time_alpha(sec: int) -> str:
    if sec < 60:
        return f"{sec}S"
    if sec < 3600:
        return f"{int(sec / 60)}M"
    return "60M+"

# Format the AUTO_DELETE_TIME to human-readable format
AUTO_DELETE_STR = format_time(AUTO_DELETE_TIME)

# Store the start time of the bot
startTime = time()

markup = None

# Function to generate invite links and create the bot's markup
async def build(_):
    global markup
    if not markup:
        chats = await get_chats(_)
        new_invite_links = []
        
        # Generate invite links for each chat
        for chat in chats:
            invite_link = await _.create_chat_invite_link(chat.id, creates_join_request=True)
            new_invite_links.append(invite_link.invite_link)
        
        # Attach invite links to chats
        for i, invite_link in enumerate(new_invite_links):
            chats[i].invite_link = invite_link
        
        # Create the markup with buttons
        chat = chats[0]
        chat1 = chats[1]
        markup = IKM(
            [
                [
                    IKB("ᴘᴏsᴛɪɴɢ ᴄʜᴀɴɴᴇʟ", url=chat.invite_link),
                    IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=chat1.invite_link)
                ],
                [
                    IKB('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ', url=TUTORIAL_LINK)
                ]
            ]
        )
    return markup
