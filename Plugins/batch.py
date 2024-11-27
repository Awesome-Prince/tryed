from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from config import SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID, LOG_CHANNEL_ID, LINK_GENERATE_IMAGE
from .encode_decode import encrypt, Int2Char
from templates import LINK_GEN
from . import alpha_grt
from Database.count_2 import incr_count_2
from Database.count import incr_count
from Database.settings import get_settings
from Database.encr import update
from . import tryer
import asyncio

dic = {}

TASK = None

def get_TASK():
    global TASK
    return TASK.done() if TASK else False

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
        return await m.reply('**Batch UnderProcess. Use /cancel to stop it.**')
    
    if not get_TASK():
        return await m.reply('Wait until the current batch is complete.')
    
    dic[m.from_user.id] = []
    await m.reply('**Batch started. Use /end when done.**', quote=True)


async def batch_cwf(_, m):
    if m.text and not m.text.startswith('/'):
        if m.from_user.id in dic:
            dic[m.from_user.id].append(m)

@Client.on_message(filters.command('cancel') & filters.user(SUDO_USERS) & filters.private)
async def cancel(_, m):
    if m.from_user.id not in dic:
        return await m.reply('No batch to cancel.')
    
    dic.pop(m.from_user.id)
    await m.reply('Batch cancelled.')

async def process_batch(_, m):
    ms = dic.get(m.from_user.id, [])
    dic.pop(m.from_user.id)
    
    if not ms:
        return await m.reply("No content to process.")
    
    # Send "processing" message
    progress_msg = await m.reply("**It takes a few minutes...**")
    
    dest_ids = []
    dest_ids_2 = []
    all_vid = True
    for x in ms:
        if not x.video:
            all_vid = False
        new = await tryer(x.copy, DB_CHANNEL_ID, caption="#batch")
        dest_ids.append(new.id)
        new = await tryer(x.copy, DB_CHANNEL_2_ID, caption="#batch")
        dest_ids_2.append(new.id)
    
    # Calculate video duration if all are videos
    duration = "⋞⋮⋟ " + alpha_grt(sum([x.video.duration for x in ms])) if all_vid else ''
    
    cur = await incr_count()
    encr = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    encr_2 = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    await update(encr, encr_2)
    
    # Generate batch link
    link = f'https://t.me/{(await get_me(_)).username}?start=batchone{encr}'
    txt = LINK_GEN.format(f'{cur}', duration, link)
    
    markup = IKM([[IKB('Share', url=link)]])
    settings = await get_settings()
    
    await progress_msg.delete()
    
    # Send link to the user
    if LINK_GENERATE_IMAGE and settings['image']:
        await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup, quote=True)
        if LOG_CHANNEL_ID and settings.get('logs', True):
            await _.send_photo(LOG_CHANNEL_ID, LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
    else:
        await m.reply(txt, reply_markup=markup, quote=True)
        if LOG_CHANNEL_ID and settings.get('logs', True):
            await _.send_message(LOG_CHANNEL_ID, txt, reply_markup=markup)

@Client.on_message(filters.command('end') & filters.user(SUDO_USERS) & filters.private)
async def end(_, m):
    global TASK
    TASK = asyncio.create_task(process_batch(_, m))
    await TASK
