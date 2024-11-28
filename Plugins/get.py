import asyncio
import os
import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ConnectionError
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from Database.sessions import get_session
from Database.privileges import get_privileges
from Database.settings import get_settings
from Database.count_2 import incr_count_2
from Database.auto_delete_2 import update_2
from config import (
    API_ID,
    API_HASH,
    DB_CHANNEL_ID,
    SUDO_USERS,
    USELESS_IMAGE,
    AUTO_SAVE_CHANNEL_ID
)
from templates import LINK_GEN, AUTO_DELETE_TEXT, USELESS_MESSAGE
from .encode_decode import *
from . import tryer, AUTO_DELETE_STR, build
from main import ClientLike

# Inline keyboard markup for share button
markup = IKM([[IKB('𝘚𝘩𝘢𝘳𝘦 𝘞𝘪𝘵𝘩 𝘔𝘦', callback_data='sharewithme')]])

# List to track ongoing downloads
og = []

# Decorator to handle exceptions and clean up
def dec(func):
    async def wrapper(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception:
            if message.from_user.id in og:
                og.remove(message.from_user.id)
            return 69
    return wrapper

@dec
async def get(client: Client, message: Message):
    """
    Download and send a specific message from a channel.
    """
    user_id = message.from_user.id
    if user_id in og:
        return await message.reply('**Wait Until Previous Download Finished.**')

    priv = await get_privileges(user_id)
    if not priv[1]:
        return await message.reply_photo(USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(client))

    session = await get_session(user_id)
    if not session:
        return await message.reply("**Before Use.You Have to Connect with Bot.For Connect Use: /connect **")

    try:
        if message.text.startswith("https://t.me/c"):
            channel = int("-100" + message.text.split("/")[-2])
            msg_id = int(message.text.split("/")[-1])
        elif message.text.startswith("https://t.me"):
            channel = message.text.split("/")[-2]
            msg_id = int(message.text.split("/")[-1])
    except Exception:
        return await message.reply('Link Is Invalid..')

    cyapa = await message.reply('Under Processing...')
    try:
        app = ClientLike(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        await app.start()
    except FloodWait as e:
        return await cyapa.edit(f'Try Again After {e.value} seconds.')
    except Exception:
        return await cyapa.edit('**Signal Lost\n\nType: /connect to restart.**')

    og.append(user_id)
    msg = await app.get_messages(channel, msg_id)
    settings = await get_settings()

    if msg.text:
        cop = await message.reply(msg.text, reply_markup=markup)
    else:
        try:
            dl = await msg.download()
            try:
                await app.stop()
            except ConnectionError:
                pass

            if msg.document:
                cop = await message.reply_document(dl, caption=msg.caption, reply_markup=markup)
            elif msg.video:
                cop = await message.reply_video(dl, caption=msg.caption, reply_markup=markup)
            elif msg.photo:
                cop = await message.reply_photo(dl, caption=msg.caption, reply_markup=markup)
            elif msg.animation:
                cop = await message.reply_animation(dl, caption=msg.caption, reply_markup=markup)
            else:
                return await cyapa.edit('This Link can\'t be accessed.')

            os.remove('downloads/' + dl.split('/')[-1])
        except Exception as e:
            og.remove(user_id)
            return await cyapa.edit(f'This Link can\'t be accessed due to: `{e}`')

    if settings['auto_save']:
        await cop.copy(AUTO_SAVE_CHANNEL_ID, reply_markup=None)

    count = await incr_count_2()
    ok = await message.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
    await update_2(user_id, [cop.id, ok.id, count, time.time()])

    await cyapa.delete()
    og.remove(user_id)
    return True

# List to track ongoing batch processes
pbd = []

@Client.on_message(filters.command('batch') & ~filters.user(SUDO_USERS) & filters.private)
async def pbatch(client: Client, message: Message):
    """
    Download and send a batch of messages from a channel.
    """
    user_id = message.from_user.id
    if user_id in pbd:
        return await message.reply("**Wait Until Previous Batch Gets Done.**")

    priv = await get_privileges(message.from_user.id)
    sets = await get_settings()
    if not priv[0]:
        return await message.reply_photo(USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(client))

    session = await get_session(user_id)
    if not session:
        return await message.reply("**Before Use.You Have to Connect with Bot.For Connect Use: /connect **")

    spl = message.text.split()
    try:
        link1 = spl[1]
    except IndexError:
        return await message.reply('Usage: /batch [starting_link] [ending_link]\n<pre>If you just give the startlink then the bot will automatically save a batch of 20 files.</pre>')
    
    try:
        link2 = spl[2]
    except IndexError:
        link2 = '/'.join(link1.split('/')[:-1]) + '/' + str(int(link1.split('/')[-1]) + 20)

    st = int(link1.split('/')[-1])
    en = int(link2.split('/')[-1]) + 1
    try:
        channel = int('-100' + link1.split('/')[-2])
    except ValueError:
        channel = link1.split('/')[-2]

    try:
        app = ClientLike(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        await app.start()
    except FloodWait as e:
        return await message.reply(f'Try Again After {e.value} seconds.')
    except Exception:
        return await message.reply('**Signal Lost\nType: /connect to Restart..**')

    pbd.append(user_id)
    messages = await app.get_messages(channel, list(range(st, en)))
    dest_ids = []
    m_e = await tryer(message.reply, 'Processing Files...')
    total = len(messages)
    DB_CHANNEL_ID = message.from_user.id
    for idx, msg in enumerate(messages, 1):
        if msg.text:
            cop = await tryer(client.send_message, DB_CHANNEL_ID, msg.text, reply_markup=markup)
        else:
            try:
                dl = await msg.download()
                if msg.document:
                    cop = await tryer(client.send_document, DB_CHANNEL_ID, dl, caption=msg.caption, reply_markup=markup)
                elif msg.video:
                    cop = await tryer(client.send_video, DB_CHANNEL_ID, dl, caption=msg.caption, reply_markup=markup)
                elif msg.photo:
                    cop = await tryer(client.send_photo, DB_CHANNEL_ID, dl, caption=msg.caption, reply_markup=markup)
                elif msg.animation:
                    cop = await tryer(client.send_animation, DB_CHANNEL_ID, dl, caption=msg.caption, reply_markup=markup)
                os.remove('downloads/' + dl.split('/')[-1])
            except Exception as e:
                pass
        dest_ids.append(cop)
        await tryer(m_e.edit, f'Processing.. `{idx}/{total}`...')

    await tryer(m_e.delete)
    try:
        await app.stop()
    except ConnectionError:
        pass

    count = await incr_count_2()
    ok = await message.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
    await update_2(user_id, [[x.id for x in dest_ids], ok.id, count, time.time()])
    pbd.remove(user_id) if user_id in pbd else None

    if sets['auto_save']:
        for x in dest_ids:
            await tryer(x.copy, AUTO_SAVE_CHANNEL_ID, reply_markup=None)