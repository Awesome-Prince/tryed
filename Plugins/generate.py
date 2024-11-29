from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from pyrogram.errors import FloodWait
from config import SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID, LOG_CHANNEL_ID, LINK_GENERATE_IMAGE
from Database.count import incr_count
from Database.settings import get_settings
from .encode_decode import encrypt, Int2Char
from .watchers import get_me
from templates import LINK_GEN
from Database import tryer
import asyncio

@Client.on_message(filters.command('gen') & filters.user(SUDO_USERS))
async def generate(_, m):
    try:
        st = int(m.text.split()[1])
        en = int(m.text.split()[2])
    except:
        return await m.reply('Usage: `/gen [start_id] [end_id]`')
    
    okkie = await m.reply("**Rendering...**")
    mess_ids = []
    
    while en - st + 1 > 200:
        mess_ids.append(list(range(st, st + 200)))
        st += 200
    if en - st + 1 > 0:
        mess_ids.append(list(range(st, en + 1)))
    
    messes = []
    for ids in mess_ids:
        messes += (await _.get_messages(DB_CHANNEL_ID, ids))
    
    await tryer(okkie.edit, "**Generating Links...**")
    settings = await get_settings()
    batches = []
    temp = []
    
    for msg in messes:
        if msg and not msg.empty:
            temp.append(msg)
        if len(temp) == settings['generate']:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)
    
    image = settings['image']
    
    for batch in batches:
        init = batch[0].id
        final = batch[-1].id
        cur = await incr_count()
        encr = encrypt(f'{Int2Char(init)}-{Int2Char(final)}|{Int2Char(cur)}')
        link = f'https://t.me/{(await get_me(_)).username}?start=batchone{encr}'
        txt = LINK_GEN.format(f'{cur}', '', link)
        markup = IKM([[IKB('Share', url=link)]])
        
        try:
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID:
                await msg.copy(LOG_CHANNEL_ID)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID and settings.get('logs', True):
                await msg.copy(LOG_CHANNEL_ID)
    
    await tryer(okkie.delete)
    await tryer(m.reply, "**Generation Completed.**", quote=True)

@Client.on_message(filters.command('gen2') & filters.user(SUDO_USERS))
async def generate2(_, m):
    try:
        st = int(m.text.split()[1])
        en = int(m.text.split()[2])
    except:
        return await m.reply('Usage: `/gen2 [start_id] [end_id]`')
    
    okkie = await m.reply("**Rendering...**")
    mess_ids = []
    
    while en - st + 1 > 200:
        mess_ids.append(list(range(st, st + 200)))
        st += 200
    if en - st + 1 > 0:
        mess_ids.append(list(range(st, en + 1)))
    
    messes = []
    for ids in mess_ids:
        messes += (await _.get_messages(DB_CHANNEL_2_ID, ids))
    
    await tryer(okkie.edit, "**Generating Links...**")
    settings = await get_settings()
    batches = []
    temp = []
    
    for msg in messes:
        if msg and not msg.empty:
            temp.append(msg)
        if len(temp) == settings['generate']:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)
    
    image = settings['image']
    
    for batch in batches:
        init = batch[0].id
        final = batch[-1].id
        cur = await incr_count()
        encr = encrypt(f'{Int2Char(init)}-{Int2Char(final)}|{Int2Char(cur)}')
        link = f'https://t.me/{(await get_me(_)).username}?start=batchtwo{encr}'
        txt = LINK_GEN.format(f'{cur}', '', link)
        markup = IKM([[IKB('Share', url=link)]])
        
        try:
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID:
                await msg.copy(LOG_CHANNEL_ID)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID and settings.get('logs', True):
                await msg.copy(LOG_CHANNEL_ID)
    
    await tryer(okkie.delete)
    await tryer(m.reply, "**Generation Completed.**", quote=True)

if DB_CHANNEL_2_ID > 0:
    @Client.on_message(filters.command('id') & filters.user(DB_CHANNEL_2_ID) & filters.private)
    async def idddd(_, m):
        reply = m.reply_to_message
        if not reply:
            return await m.reply('Reply to a message.')
        await m.reply(reply.id)
