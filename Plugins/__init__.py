import asyncio
from time import time
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
)
from config import Config  # Import the Config class from config.py
from .start import get_chats

# Helper function to retry a function call if it raises a FloodWait error
async def tryer(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)

# Convert seconds to a human-readable format
def grt(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}S"
    if seconds < 3600:
        return f"{int(seconds/60)}M"
    return f"{int(seconds/3600)}H"

def alpha_grt(sec: int) -> str:
    if sec < 60:
        return f"{sec}S"
    if sec < 3600:
        return f"{int(sec/60)}M"
    return "60M+"

# Constants
AUTO_DELETE_STR = grt(Config.AUTO_DELETE_TIME)
startTime = time()

# Global variable for inline keyboard markup
markup = None

# Function to build the inline keyboard markup
async def build(_):
    global markup
    if not markup:
        chats = await get_chats(_)
        new_links = []
        for chat in chats:
            invite_link = await _.create_chat_invite_link(chat.id, creates_join_request=True)
            new_links.append(invite_link.invite_link)
        
        for chat, link in zip(chats, new_links):
            chat.invite_link = link
        
        chat_posting = chats[0]
        chat_backup = chats[1]
        
        markup = IKM(
            [
                [
                    IKB("ᴘᴏsᴛɪɴɢ ᴄʜᴀɴɴᴇʟ", url=chat_posting.invite_link),
                    IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=chat_backup.invite_link)
                ],
                [
                    IKB('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ', url=Config.TUTORIAL_LINK)
                ]
            ]
        )
    return markup
