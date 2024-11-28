import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from Database.auto_delete import update, get
from Database.privileges import get_privileges
from Database.sessions import get_session
from Database.encr import get_encr
from Database.users import add_user, is_user
from templates import AUTO_DELETE_TEXT, START_MESSAGE, START_MESSAGE_2, TRY_AGAIN_TEXT
from config import (
    DB_CHANNEL_ID, 
    DB_CHANNEL_2_ID, 
    FSUB_1, 
    FSUB_2, 
    STICKER_ID, 
    AUTO_DELETE_TIME, 
    CONTENT_SAVER, 
    TUTORIAL_LINK
)
from .encode_decode import decrypt, Char2Int
from .block import block_dec
from . import AUTO_DELETE_STR, tryer, build
from main import app

# List of subscription channels
FSUB = [FSUB_1, FSUB_2]

# Dictionary to keep track of members
members = {FSUB_1: [], FSUB_2: []}

@Client.on_chat_member_updated(filters.chat(FSUB))
async def cmufunc(client: Client, chat_member_update: ChatMemberUpdated):
    """
    Track users joining or leaving the subscription channels.
    """
    joined = chat_member_update.new_chat_member and not chat_member_update.old_chat_member
    left = chat_member_update.old_chat_member and not chat_member_update.new_chat_member
    if joined:
        members[chat_member_update.chat.id].append(chat_member_update.from_user.id)
    elif left:
        try:
            members[chat_member_update.chat.id].remove(chat_member_update.from_user.id)
        except ValueError:
            pass

async def check_fsub(user_id: int) -> bool:
    """
    Check if a user is subscribed to all required channels.
    """
    for y in FSUB:
        if user_id not in members[y]:
            try:
                chat_member = await tryer(app.get_chat_member, y, user_id)
                if chat_member.status.name not in ["ADMINISTRATOR", "OWNER", "MEMBER"]:
                    return False
            except Exception:
                return False
            members[y].append(user_id)
    return True

me = None
chats = []

async def get_chats(client: Client):
    """
    Get the subscription channels and generate invite links.
    """
    global chats
    if not chats:
        chats = [await client.get_chat(FSUB_1), await client.get_chat(FSUB_2)]
        new_links = []
        for chat in chats:
            invite_link = await client.create_chat_invite_link(chat.id, creates_join_request=True)
            new_links.append(invite_link.invite_link)
        for idx, chat in enumerate(chats):
            chat.invite_link = new_links[idx]
    return chats

async def markup(client: Client, link=None) -> IKM:
    """
    Generate an inline keyboard markup for channel subscription links.
    """
    chats = await get_chats(client)
    buttons = [
        IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[0].invite_link),
        IKB('ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ', url=chats[1].invite_link)
    ]
    markup_buttons = [buttons]
    if link:
        markup_buttons.append([IKB('ᴛʀʏ ᴀɢᴀɪɴ♻️', url=link)])
    return IKM(markup_buttons)

async def start_markup(client: Client) -> IKM:
    """
    Generate an inline keyboard markup for the start message.
    """
    chats = await get_chats(client)
    buttons = [
        IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[0].invite_link),
        IKB('ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ', url=chats[1].invite_link)
    ]
    markup_buttons = [buttons, [IKB('ᴜsᴇ ᴍᴇ ᴛᴜᴛᴏʀɪᴀʟ', url=TUTORIAL_LINK)]]
    return IKM(markup_buttons)

control_batch = []

@block_dec
async def start(client: Client, message: Message):
    """
    Handle the start command and manage batch processing.
    """
    global me, chats
    if not me:
        me = await client.get_me()
    user_id = message.from_user.id
    chats = await get_chats(client)
    if not await is_user(user_id):
        await add_user(user_id)
        return await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=await start_markup(client))
    
    prem = (await get_privileges(user_id))[2] if CONTENT_SAVER else True
    txt = message.text.split()
    if len(txt) > 1:
        command = txt[1]
        if command.startswith('get'):
            encr = command[3:]
            for chat in chats:
                if not await check_fsub(user_id):
                    mark = await markup(client, f'https://t.me/{me.username}?start=get{encr}')
                    return await message.reply(TRY_AGAIN_TEXT.format(message.from_user.mention), reply_markup=mark)
            
            std = await message.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')
            msg = await client.get_messages(DB_CHANNEL_ID, Char2Int(spl[0]))
            if msg.empty:
                msg = await client.get_messages(DB_CHANNEL_2_ID, Char2Int(spl[2]))
            await std.delete()
            if not prem:
                ok = await msg.copy(message.from_user.id, caption=None, reply_markup=None, protect_content=True)
            else:
                ok = await msg.copy(message.from_user.id, caption=None, reply_markup=None)
            if AUTO_DELETE_TIME != 0:
                ok1 = await ok.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                dic = await get(message.from_user.id)
                dic[str(ok.id)] = [str(ok1.id), time(), f'https://t.me/{me.username}?start=get{encr}']
                await update(message.from_user.id, dic)
            return
            
            if command.startswith('batchone'):
            encr = command[8:]
            for chat in chats:
                if not await check_fsub(user_id):
                    mark = await markup(client, f'https://t.me/{me.username}?start=batchone{encr}')
                    return await message.reply(TRY_AGAIN_TEXT.format(message.from_user.mention), reply_markup=mark)
            
            std = await message.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')[0].split('-')
            st = Char2Int(spl[0])
            en = Char2Int(spl[1])
            messes = [await client.get_messages(DB_CHANNEL_ID, st)] if st == en else []
            if not messes:
                new_encr = await get_encr(encr)
                if new_encr:
                    spl = decrypt(new_encr).split('|')[0].split('-')
                    st = Char2Int(spl[0])
                    en = Char2Int(spl[1])
                    if st == en:
                        messes = [await client.get_messages(DB_CHANNEL_2_ID, st)]
                    else:
                        mess_ids = []
                        while en - st + 1 > 200:
                            mess_ids.append(list(range(st, st + 200)))
                            st += 200
                        if en - st + 1 > 0:
                            mess_ids.append(list(range(st, en + 1)))
                        for ids in mess_ids:
                            messes += await client.get_messages(DB_CHANNEL_2_ID, ids)
            if len(messes) > 10:
                okkie = await message.reply("It's Take Few Seconds...")
            haha = []
            if not prem:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None, protect_content=True)
                    haha.append(gg)
                    await asyncio.sleep(1)
            else:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None)
                    haha.append(gg)
                    await asyncio.sleep(1)
            await std.delete()
            if AUTO_DELETE_TIME != 0:
                ok1 = await message.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                dic = await get(message.from_user.id)
                for ok in haha:
                    if not ok:
                        continue
                    dic[str(ok.id)] = [str(ok1.id), time(), f'https://t.me/{me.username}?start=batchone{encr}']
                await update(message.from_user.id, dic)
            if okkie:
                await okkie.delete()
            return
        elif command.startswith('batchtwo'):
            encr = command[8:]
            for chat in chats:
                if not await check_fsub(user_id):
                    mark = await markup(client, f'https://t.me/{me.username}?start=batchtwo{encr}')
                    return await message.reply(TRY_AGAIN_TEXT.format(message.from_user.mention), reply_markup=mark)
            std = await message.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')[0].split('-')
            st = Char2Int(spl[0])
            en = Char2Int(spl[1])
            if st == en:
                messes = [await client.get_messages(DB_CHANNEL_2_ID, st)]
            else:
                mess_ids = []
                while en - st + 1 > 200:
                    mess_ids.append(list(range(st, st + 200)))
                    st += 200
                if en - st + 1 > 0:
                    mess_ids.append(list(range(st, en+1)))
                messes = []
                for ids in mess_ids:
                    messes += await client.get_messages(DB_CHANNEL_2_ID, ids)
            okkie = None
            if len(messes) > 10:
                okkie = await message.reply("It's Take Few Seconds....")
            haha = []
            if not prem:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None, protect_content=True)
                    haha.append(gg)
                    await asyncio.sleep(1)
            else:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None)
                    haha.append(gg)
                    await asyncio.sleep(1)
            await std.delete()
            if AUTO_DELETE_TIME != 0:
                ok1 = await message.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                dic = await get(message.from_user.id)
                for ok in haha:
                    if not ok:
                        continue
                    dic[str(ok.id)] = [str(ok1.id), time(), f'https://t.me/{me.username}?start=batchtwo{encr}']
                await update(message.from_user.id, dic)
            if okkie:
                await okkie.delete()
            return
    else:
        await message.reply(START_MESSAGE_2.format(message.from_user.mention), reply_markup=await start_markup(client))

@Client.on_message(filters.command('start') & filters.private)
async def start_func(_, m):
    user_id = m.from_user.id
    if user_id in control_batch:
        return
    control_batch.append(user_id)
    try:
        await start(_, m)
    except Exception:
        pass
    control_batch.remove(user_id) if user_id in control_batch else None
    elif command.startswith('batchtwo'):
            encr = command[8:]
            for chat in chats:
                if not await check_fsub(user_id):
                    mark = await markup(client, f'https://t.me/{me.username}?start=batchtwo{encr}')
                    return await message.reply(TRY_AGAIN_TEXT.format(message.from_user.mention), reply_markup=mark)
            std = await message.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')[0].split('-')
            st = Char2Int(spl[0])
            en = Char2Int(spl[1])
            if st == en:
                messes = [await client.get_messages(DB_CHANNEL_2_ID, st)]
            else:
                mess_ids = []
                while en - st + 1 > 200:
                    mess_ids.append(list(range(st, st + 200)))
                    st += 200
                if en - st + 1 > 0:
                    mess_ids.append(list(range(st, en+1)))
                messes = []
                for ids in mess_ids:
                    messes += await client.get_messages(DB_CHANNEL_2_ID, ids)
            okkie = None
            if len(messes) > 10:
                okkie = await message.reply("It's Take Few Seconds....")
            haha = []
            if not prem:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None, protect_content=True)
                    haha.append(gg)
                    await asyncio.sleep(1)
            else:
                for msg in messes:
                    if msg.empty:
                        continue
                    gg = await tryer(msg.copy, message.from_user.id, caption=None, reply_markup=None)
                    haha.append(gg)
                    await asyncio.sleep(1)
            await std.delete()
            if AUTO_DELETE_TIME != 0:
                ok1 = await message.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                dic = await get(message.from_user.id)
                for ok in haha:
                    if not ok:
                        continue
                    dic[str(ok.id)] = [str(ok1.id), time(), f'https://t.me/{me.username}?start=batchtwo{encr}']
                await update(message.from_user.id, dic)
            if okkie:
                await okkie.delete()
            return
    else:
        await message.reply(START_MESSAGE_2.format(message.from_user.mention), reply_markup=await start_markup(client))

@Client.on_message(filters.command('start') & filters.private)
async def start_func(_, m):
    user_id = m.from_user.id
    if user_id in control_batch:
        return
    control_batch.append(user_id)
    try:
        await start(_, m)
    except Exception:
        pass
    control_batch.remove(user_id) if user_id in control_batch else None
