from time import time
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
)
from config import TUTORIAL_LINK, AUTO_DELETE_TIME
from .start import get_chats

# Function to handle FloodWait exceptions
async def tryer(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)

# Function to convert seconds to human-readable format
def grt(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}S"
    if seconds < 3600:
        return f"{int(seconds / 60)}M"
    return f"{int(seconds / 3600)}H"

# Alternate function to convert seconds to human-readable format
def alpha_grt(sec: int) -> str:
    if sec < 60:
        return f"{sec}S"
    if sec < 3600:
        return f"{int(sec / 60)}M"
    return "60M+"

# Convert AUTO_DELETE_TIME to human-readable format
AUTO_DELETE_STR = grt(AUTO_DELETE_TIME)

# Record the start time
startTime = time()

# Global variable for markup
markup = None

# Function to build inline keyboard markup
async def build(_):
    global markup
    if not markup:
        chats = await get_chats(_)
        invite_links = []
        for chat in chats:
            invite_link = await _.create_chat_invite_link(chat.id, creates_join_request=True)
            invite_links.append(invite_link.invite_link)
        for chat, link in zip(chats, invite_links):
            chat.invite_link = link
        chat1, chat2 = chats[:2]
        markup = IKM(
            [
                [
                    IKB("ᴘᴏsᴛɪɴɢ ᴄʜᴀɴɴᴇʟ", url=chat1.invite_link),
                    IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=chat2.invite_link)
                ],
                [
                    IKB('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ', url=TUTORIAL_LINK)
                ]
            ]
        )
    return markup
