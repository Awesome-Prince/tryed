from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from config import SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID, LOG_CHANNEL_ID, LINK_GENERATE_IMAGE
from .encode_decode import encrypt, Int2Char
from templates import LINK_GEN
from Database.count_2 import incr_count_2
from Database.count import incr_count
from Database.settings import get_settings
from Database.encr import update
from Database import tryer
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

@Client.on_message(filters.text & filters.user(SUDO_USERS) & filters.private)
async def batch_cwf(_, m):
    if m.text and not m.text.startswith('/') and m.from_user.id in dic:
        dic[m.from_user.id].append(m)

@Client.on_message(filters.command('cancel') & filters.user(SUDO_USERS) & filters.private)
async def cancel(_, m):
    if m.from_user.id not in dic:
        return await m.reply('Nothing to cancel.')
    dic.pop(m.from_user.id)
    await m.reply('Batch Cancelled.')

async def end(_, m):
    if m.from_user.id not in dic:
        return
    ms = dic.pop(m.from_user.id)
    if not ms:
        return
    iffff = await m.reply("**It Takes Few Minutes..**")
    dest_ids, dest_ids_2 = [], []
    all_vid = all(x.video for x in ms)
    for x in ms:
        new = await tryer_with_retry(x.copy, DB_CHANNEL_ID, caption="#batch")
        dest_ids.append(new.id)
        new = await tryer_with_retry(x.copy, DB_CHANNEL_2_ID, caption="#batch")
        dest_ids_2.append(new.id)
    duration = f"⋞⋮⋟ {alpha_grt(sum(x.video.duration for x in ms))}" if all_vid else ''
    cur = await incr_count()
    encr = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    encr_2 = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    await update(encr, encr_2)
    link = f'https://t.me/{(await get_me(_)).username}?start=batchone{encr}'
    txt = LINK_GEN.format(f'{cur}', duration, link)
    markup = IKM([[IKB('Share', url=link)]])
    settings = await get_settings()
    await iffff.delete()
    if LINK_GENERATE_IMAGE and settings['image']:
        await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup, quote=True)
        if LOG_CHANNEL_ID and settings.get('logs', True):
            await _.send_photo(LOG_CHANNEL_ID, LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
    else:
        await m.reply(txt, reply_markup=markup, quote=True)
        if LOG_CHANNEL_ID and settings.get('logs', True):
            await _.send_message(LOG_CHANNEL_ID, txt, reply_markup=markup)

@Client.on_message(filters.command('end') & filters.user(SUDO_USERS) & filters.private)
async def endddd(_, m):
    global TASK
    TASK = asyncio.create_task(end(_, m))
    await TASK

async def tryer_with_retry(func, *args, **kwargs):
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)  # Wait for the specified time plus 1 second as a buffer
