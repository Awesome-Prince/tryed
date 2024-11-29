from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from config import SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID, LOG_CHANNEL_ID, LINK_GENERATE_IMAGE
from .encode_decode import encrypt, Int2Char
from templates import LINK_GEN
from Database.count_2 import incr_count_2
from Database.count import incr_count
from Database.settings import get_settings
from Database.encr import update
from Database import tryer  # Correct import
import asyncio

dic = {}
me = None

class bkl:
    @staticmethod
    def done():
        return True

TASK = bkl

def get_TASK():
    return TASK.done()

async def get_me(_):
    global me
    if not me:
        me = await _.get_me()
    return me
  
def in_batch(user_id):
    return user_id in dic or not get_TASK()

@Client.on_message(filters.command('b') & filters.user(SUDO_USERS) & filters.private)
async def batch(_, m):
    if m.from_user.id in dic:
        return await m.reply('**Batch UnderProcess Use /cancel For Stop!!.** ')
    if TASK and not TASK.done():
        return await m.reply('Wait Until The Batch Gets Done.')
    dic[m.from_user.id] = []
    await m.reply('**OKAY Now I Can Make Batch Link When You Done Use /end **', quote=True)

@Client.on_message
