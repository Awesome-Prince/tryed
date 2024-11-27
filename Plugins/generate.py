import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from pyrogram.errors import FloodWait
from Database.count import incr_count
from Database.settings import get_settings
from .encode_decode import encrypt, Int2Char
from .watchers import get_me
from templates import LINK_GEN
from config import SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID, LOG_CHANNEL_ID, LINK_GENERATE_IMAGE
from . import tryer

async def generate_links(_, m, db_channel_id, batch_prefix):
    try:
        st = int(m.text.split()[1])
        en = int(m.text.split()[2])
    except (IndexError, ValueError):
        return await m.reply('Usage: `/gen [start_id] [end_id]`')

    okkie = await m.reply("**Rendering...**")
    
    # Split IDs into manageable chunks of 200
    mess_ids = [list(range(st + i * 200, min(st + (i + 1) * 200, en + 1))) for i in range((en - st + 1) // 200 + 1)]
    
    # Get the messages from the DB channel
    messes = []
    for ids in mess_ids:
        messes += await _.get_messages(db_channel_id, ids)

    await tryer(okkie.edit, "**Generating Links...**")
    settings = await get_settings()

    batches = []
    temp = []
    for x in messes:
        if x and not x.empty:
            temp.append(x)
        if len(temp) == settings['generate']:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)

    # Generate links for each batch
    image = settings['image']
    for x in batches:
        init, final = x[0].id, x[-1].id
        cur = await incr_count()
        encr = encrypt(f'{Int2Char(init)}-{Int2Char(final)}|{Int2Char(cur)}')
        link = f'https://t.me/{(await get_me(_)).username}?start={batch_prefix}{encr}'
        txt = LINK_GEN.format(f'{cur}', '', link)
        markup = IKM([[IKB('Share', url=link)]])
        
        try:
            msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup) if LINK_GENERATE_IMAGE and image else await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID:
                await msg.copy(LOG_CHANNEL_ID)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup) if LINK_GENERATE_IMAGE and image else await m.reply(txt, reply_markup=markup)
            if LOG_CHANNEL_ID and settings.get('logs', True):
                await msg.copy(LOG_CHANNEL_ID)

    await tryer(okkie.delete)
    await tryer(m.reply, "**Generation Completed.**", quote=True)


@Client.on_message(filters.command('gen') & filters.user(SUDO_USERS))
async def generate(_, m):
    await generate_links(_, m, DB_CHANNEL_ID, 'batchone')


@Client.on_message(filters.command('gen2') & filters.user(SUDO_USERS))
async def generate2(_, m):
    await generate_links(_, m, DB_CHANNEL_2_ID, 'batchtwo')


# Handle /id command from DB_CHANNEL_2_ID
if DB_CHANNEL_2_ID > 0:
    @Client.on_message(filters.command('id') & filters.user(DB_CHANNEL_2_ID) & filters.private)
    async def idddd(_, m):
        reply = m.reply_to_message
        if not reply:
            return await m.reply('Reply to a message.')
        await m.reply(reply.id)
