from time import time
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import TUTORIAL_LINK, AUTO_DELETE_TIME
from helpers import get_chats
from Database import tryer

def grt(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}S"
    if seconds < 3600:
        return f"{int(seconds / 60)}M"
    return f"{int(seconds / 3600)}H"

def alpha_grt(sec: int) -> str:
    if sec < 60:
        return f"{sec}S"
    if sec < 3600:
        return f"{int(sec / 60)}M"
    return "60M+"

AUTO_DELETE_STR = grt(AUTO_DELETE_TIME)
startTime = time()

markup = None

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
                    IKB("Posting Channel", url=chat1.invite_link),
                    IKB("Backup Channel", url=chat2.invite_link)
                ],
                [
                    IKB('How to use Terabox Bot', url=TUTORIAL_LINK)
                ]
            ]
        )
    return markup

me = None

async def get_me(_):
    global me
    if not me:
        me = await _.get_me()
    return me
