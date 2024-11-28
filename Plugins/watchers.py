from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
)
from config import (
    SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID,
    LOG_CHANNEL_ID, LINK_GENERATE_IMAGE,
    USELESS_IMAGE,
    TUTORIAL_LINK
)
from templates import USELESS_MESSAGE, LINK_GEN
from .encode_decode import encrypt, Int2Char
from Database.count import incr_count
from Database.settings import get_settings
from .batch import in_batch, batch_cwf as bcwf
from .block import block_dec
from . import alpha_grt, tryer
from pyrogram.errors import FloodWait
import asyncio
from .connect import in_work
from .get import get
from . import build

watch = 1

me = None

async def get_me(client: Client):
    """
    Get the bot's own user information.
    """
    global me
    if not me:
        me = await client.get_me()
    return me

@Client.on_message(filters.private, group=watch)
@block_dec
async def cwf(client: Client, message: Message):
    """
    Handle incoming private messages and perform necessary actions.
    """
    if in_work(message.from_user.id):
        return
    if in_batch(message.from_user.id):
        return await bcwf(client, message)
    if message.text and message.text.startswith("https://t.me/"):
        ret = await get(client, message)
        if ret:
            return
    if message.from_user.id not in SUDO_USERS:
        if message.text:
            if not message.text.lower().startswith(('/start', '/terminate', '/connect', '/bot', '..', '/batch', '/id')):
                markup = await build(client)
                if USELESS_IMAGE:
                    await message.reply_photo(USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=markup)
                else:
                    await message.reply(USELESS_MESSAGE, reply_markup=markup)
        else:
            markup = await build(client)
            if USELESS_IMAGE:
                await message.reply_photo(USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=markup)
            else:
                await message.reply(USELESS_MESSAGE, reply_markup=markup)
        return
    if message.text and message.text.startswith('/'):
        return
    
    settings = await get_settings()

    res = await asyncio.gather(
        tryer(message.copy, DB_CHANNEL_ID),
        tryer(message.copy, DB_CHANNEL_2_ID)
    )
    
    count = await incr_count()
    encr = encrypt(f'{Int2Char(res[0].id)}|{Int2Char(count)}|{Int2Char(res[1].id)}')
    link = f'https://t.me/{(await get_me(client)).username}?start=get{encr}'
    
    if message.video:
        dur = "⋞⋮⋟ " + alpha_grt(message.video.duration)
    else:
        dur = ''
    
    txt = LINK_GEN.format(str(count), dur, link)
    markup = IKM([[IKB('Share', url=link)]])
    
    if LINK_GENERATE_IMAGE and settings['image']:
        msg = await tryer(message.reply_photo, LINK_GENERATE_IMAGE, caption=txt, quote=True)
    else:
        msg = await tryer(message.reply, txt, quote=True)
    
    if LOG_CHANNEL_ID and settings.get('logs', True):
        await tryer(msg.copy, LOG_CHANNEL_ID)