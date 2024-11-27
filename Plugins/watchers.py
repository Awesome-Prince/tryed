from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import (
    SUDO_USERS, DB_CHANNEL_ID, DB_CHANNEL_2_ID,
    LOG_CHANNEL_ID, LINK_GENERATE_IMAGE,
    USELESS_IMAGE, USELESS_MESSAGE, TUTORIAL_LINK
)
from templates import LINK_GEN
from .encode_decode import encrypt, Int2Char
from Database.count import incr_count
from Database.settings import get_settings
from .batch import in_batch, batch_cwf as bcwf
from .block import block_dec
from . import alpha_grt, tryer
from pyrogram.errors import FloodWait
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

watch = 1
me = None

async def get_me(_):
    global me
    if not me:
        me = await _.get_me()
    return me

@Client.on_message(filters.private, group=watch)
@block_dec
async def cwf(_: Client, m: Message):
    try:
        # Prevent handling messages from users in specific states
        if in_work(m.from_user.id) or in_batch(m.from_user.id):
            return await bcwf(_, m) if in_batch(m.from_user.id) else None
        
        # Handle messages with specific URLs
        if m.text and m.text.startswith("https://t.me/"):
            ret = await get(_, m)
            if ret:
                return

        # Handle non-SUDO users with custom reply
        if m.from_user.id not in SUDO_USERS:
            markup = await build(_)
            message_to_send = USELESS_MESSAGE
            if USELESS_IMAGE:
                await m.reply_photo(USELESS_IMAGE, caption=message_to_send, reply_markup=markup)
            else:
                await m.reply(message_to_send, reply_markup=markup)
            return
        
        # Skip commands like /start, /terminate, etc.
        if m.text and m.text.startswith('/'):
            return

        settings = await get_settings()

        # Image or Text for link generation
        try:
            msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption='**Generating Link...**', quote=True) if LINK_GENERATE_IMAGE and settings['image'] else await m.reply('**Generating Link...**', quote=True)
        except FloodWait as e:
            logging.warning(f"Flood wait detected: {e.value} seconds. Retrying...")
            await asyncio.sleep(e.value)
            msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption='**Generating Link...**', quote=True) if LINK_GENERATE_IMAGE and settings['image'] else await m.reply('**Generating Link...**', quote=True)

        # Copy message to channels
        res = await asyncio.gather(
            tryer(m.copy, DB_CHANNEL_ID),
            tryer(m.copy, DB_CHANNEL_2_ID)
        )

        # Increment count and generate link
        count = await incr_count()
        encr = encrypt(f'{Int2Char(res[0].id)}|{Int2Char(count)}|{Int2Char(res[1].id)}')
        link = f'https://t.me/{(await get_me(_)).username}?start=get{encr}'

        # Video duration handling
        dur = alpha_grt(m.video.duration) if m.video else ''
        txt = LINK_GEN.format(str(count), dur, link)

        # Send the final message
        markup = IKM([[IKB('Share', url=link)]])
        if LINK_GENERATE_IMAGE and settings['image']:
            await tryer(m.reply_photo, LINK_GENERATE_IMAGE, caption=txt, quote=True)
        else:
            await tryer(m.reply, txt, quote=True)

        # Log to the LOG_CHANNEL_ID if enabled
        if LOG_CHANNEL_ID and settings.get('logs', True):
            await tryer(msg.copy, LOG_CHANNEL_ID)
        
    except Exception as e:
        logging.error(f"Error in cwf function: {e}")
        try:
            # In case of any error, send a message to the user about the failure
            await m.reply("There was an error generating your link. Please try again later.")
        except Exception as inner_e:
            logging.error(f"Error while sending error message to user: {inner_e}")
