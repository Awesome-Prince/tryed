from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PasswordHashInvalid,
)
from config import API_ID, API_HASH, USELESS_IMAGE, PHONE_NUMBER_IMAGE
from Database.sessions import get_session, update_session, del_session
from Database.privileges import get_privileges
from Database import tryer  # Correct import
from . import build
from templates import USELESS_MESSAGE
import asyncio

phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘤𝘶𝘵', url='tg://settings')]])

dic = {}
watch = 69

def in_work(user_id):
    return user_id in dic

@Client.on_message(filters.command('connect') & filters.private)
async def conn(_, m):
    user_id = m.from_user.id
    priv = await get_privileges(user_id)
    if not priv[1]:
        return await tryer(m.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(_))
    
    session = await get_session(user_id)
    if session:
        app = Client(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        try:
            await app.start()
            await m.reply('**You Are Already Connected User**')
            await app.stop()
            return
        except:
            await del_session(user_id)
    
    if in_work(user_id):
        return await m.reply("**Process Ongoing..., use /terminate to cancel.**")
    
    await m.reply_photo(PHONE_NUMBER_IMAGE, caption="**Enter Your Phone Number With Country Code.**\n<pre>How To Find Number?</pre>\nUse Shortcut Button To Find Your Number\n<pre>In case Shortcut Button Not Working, Find Manually</pre>", reply_markup=phone_markup)
    cli = Client(str(user_id), api_id=API_ID, api_hash=API_HASH)
    dic[user_id] = [cli]
    await cli.connect()

@Client.on_message(filters.private, group=watch)
async def cwf(_, m):
    user_id = m.from_user.id
    if not in_work(user_id):
        return
    if not m.text or m.text.startswith("/"):
        return
    
    lis = dic[user_id]
    cli = lis[0]

    if len(lis) == 1:
        lis.append(m.text)
        try:
            hash = await cli.send_code(m.text)
        except ConnectionError:  # Use built-in ConnectionError
            await cli.connect()
            hash = await cli.send_code(m.text)
        except PhoneNumberInvalid:
            dic.pop(user_id)
            return await m.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)
        lis.append(hash.phone_code_hash)
        await m.reply("**Enter OTP:**")
        dic[user_id] = lis
    
    elif len(lis) == 3:
        txt = m.text.replace(" ", "") if " " in m.text else m.text
        lis.append(txt)
        dic[user_id] = lis
        try:
            await cli.sign_in(lis[1], lis[2], lis[3])
            session = await cli.export_session_string()
            await update_session(user_id, session)
            await cli.disconnect()
            dic.pop(user_id)
            await m.reply("**Successfully Connected..**")
        except PhoneCodeInvalid:
            dic.pop(user_id)
            return await m.reply('**Invalid OTP!**')
        except SessionPasswordNeeded:
            await m.reply("**Enter Two Step Verification Password:**")
    
    elif len(lis) == 4:
        lis.append(m.text)
        dic[user_id] = lis
        try:
            await cli.check_password(lis[4])
            await cli.sign_in(lis[1], lis[2], lis[3])
            session = await cli.export_session_string()
            await update_session(user_id, session)
            await cli.disconnect()
            dic.pop(user_id)
            await m.reply("**Connected Successfully.**")
        except PhoneCodeInvalid:
            dic.pop(user_id)
            return await m.reply('**Invalid OTP!**')
        except PasswordHashInvalid:
            dic.pop(user_id)
            return await m.reply('**Invalid Two Step Verification Password.**')

@Client.on_message(filters.command("terminate") & filters.private)
async def terminate(_, m):
    user_id = m.from_user.id
    if not in_work(user_id):
        return
    dic.pop(user_id)
    await m.reply("**Process Terminated.**")
