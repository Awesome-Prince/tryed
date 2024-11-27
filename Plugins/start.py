import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from .encode_decode import decrypt, Char2Int
from config import DB_CHANNEL_ID, AUTO_DELETE_TIME, FSUB_1, FSUB_2, DB_CHANNEL_2_ID, TUTORIAL_LINK, CONTENT_SAVER, STICKER_ID
from time import time
from Database.auto_delete import update, get
from Database.privileges import get_privileges
from helpers import tryer
from Database.users import add_user, is_user
from templates import AUTO_DELETE_TEXT, START_MESSAGE, START_MESSAGE_2, TRY_AGAIN_TEXT
from .block import block_dec
from Database.encr import get_encr
from main import app

# Set up logging
logging.basicConfig(level=logging.INFO)

members = {FSUB_1: [], FSUB_2: []}  # {chat_id: [user_id]}
FSUB = [FSUB_1, FSUB_2]
control_batch = []

me = None
chats = []

# Subscribe check function
async def check_fsub(user_id: int) -> bool:
    for y in FSUB:
        if user_id not in members[y]:
            try:
                x = await tryer(app.get_chat_member, y, user_id)
                if x.status.name not in ["ADMINISTRATOR", "OWNER", "MEMBER"]:
                    return False
            except Exception as e:
                logging.error(f"Error checking subscription: {e}")
                return False
            members[y].append(user_id)
    return True

# Fetch chat details and generate invite links
async def get_chats(_) -> list:
    global chats
    if not chats:
        try:
            chats = [await _.get_chat(FSUB_1), await _.get_chat(FSUB_2)]
            new = []
            for x in chats:
                y = await _.create_chat_invite_link(x.id, creates_join_request=True)
                new.append(y.invite_link)
            for x, y in enumerate(new):
                chats[x].invite_link = y
        except Exception as e:
            logging.error(f"Error fetching chats: {e}")
    return chats

# Generate inline keyboard markup
async def markup(_, link=None) -> IKM:
    try:
        chats = await get_chats(_)
        mark = [
            IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[0].invite_link),
            IKB('ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ', url=chats[1].invite_link)
        ]
        mark = [mark]
        if link:
            mark.append([IKB('ᴛʀʏ ᴀɢᴀɪɴ♻️', url=link)])
        return IKM(mark)
    except Exception as e:
        logging.error(f"Error generating markup: {e}")
        return IKM([])

# Generate start markup with tutorial link
async def start_markup(_) -> IKM:
    try:
        chats = await get_chats(_)
        mark = [
            IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[0].invite_link),
            IKB('ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ', url=chats[1].invite_link)
        ]
        mark = [mark]
        mark.append([IKB('ᴜsᴇ ᴍᴇ ᴛᴜᴛᴏʀɪᴀʟ', url=TUTORIAL_LINK)])
        return IKM(mark)
    except Exception as e:
        logging.error(f"Error generating start markup: {e}")
        return IKM([])

# Start function
@block_dec
async def start(_, m):
    global me, chats
    if not me:
        me = await _.get_me()

    user_id = m.from_user.id
    chats = await get_chats(_)
    if not await is_user(m.from_user.id):
        await add_user(m.from_user.id)
        return await m.reply(START_MESSAGE.format(m.from_user.mention), reply_markup=await start_markup(_))

    if CONTENT_SAVER:
        prem = (await get_privileges(m.from_user.id))[2]
    else:
        prem = True

    txt = m.text.split()
    if len(txt) > 1:
        command = txt[1]
        if command.startswith('get'):
            encr = command[3:]
            for i in chats:
                if not await check_fsub(m.from_user.id):
                    mark = await markup(_, f'https://t.me/{me.username}?start=get{encr}')
                    return await m.reply(TRY_AGAIN_TEXT.format(m.from_user.mention), reply_markup=mark)
            std = await m.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')
            try:
                msg = await _.get_messages(DB_CHANNEL_ID, Char2Int(spl[0]))
                if msg.empty:
                    msg = await _.get_messages(DB_CHANNEL_2_ID, Char2Int(spl[2]))
            except Exception as e:
                logging.error(f"Error fetching message: {e}")
                msg = await _.get_messages(DB_CHANNEL_2_ID, Char2Int(spl[2]))
            await std.delete()

            # Send message to user
            try:
                if not prem:
                    ok = await msg.copy(m.from_user.id, caption=None, reply_markup=None, protect_content=True)
                else:
                    ok = await msg.copy(m.from_user.id, caption=None, reply_markup=None)
                if AUTO_DELETE_TIME != 0:
                    ok1 = await ok.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                    dic = await get(m.from_user.id)
                    dic[str(ok.id)] = [str(ok1.id), time(), f'https://t.me/{me.username}?start=get{encr}']
                    await update(m.from_user.id, dic)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
            return

        # Handle batchone and batchtwo similarly...
    else:
        await m.reply(START_MESSAGE_2.format(m.from_user.mention), reply_markup=await start_markup(_))

# Start command handler
@Client.on_message(filters.command('start') & filters.private)
async def start_func(_, m):
    user_id = m.from_user.id
    if user_id in control_batch:  # Yeh line theek karna tha
        # Yahan apna batch process code daalein
        pass
