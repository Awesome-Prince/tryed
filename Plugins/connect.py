from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from Database.sessions import *
from Database.privileges import get_privileges
from config import API_ID, API_HASH, USELESS_IMAGE, PHONE_NUMBER_IMAGE
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PasswordHashInvalid
)
from . import build, tryer
from templates import USELESS_MESSAGE

phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘤𝘶𝘵', url='tg://settings')]])

# Dictionary to track ongoing connection processes
dic = {}
watch = 69

def in_work(user_id):
    return user_id in dic

@Client.on_message(filters.command('connect') & filters.private)
async def conn(client, message):
    user_id = message.from_user.id
    priv = await get_privileges(user_id)
    if not priv[1]:
        return await tryer(message.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(client))
    
    session = await get_session(user_id)
    if session:
        app = Client(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        try:
            await app.start()
            await message.reply('**You Are Already Connected User**')
            await app.stop()
            return
        except:
            await del_session(user_id)
    
    if user_id in dic:
        return await message.reply("**Process Ongoing..., use /terminate to cancel.**")
    
    await message.reply_photo(PHONE_NUMBER_IMAGE, caption=(
        "**Enter Your Phone Number With Country Code.\n"
        "<pre>How To Find Number?</pre>\n"
        "You can Use Shortcut Button To Find Your Number\n"
        "<pre>Incase Shortcut Button Not Working Then You Need To Find Manually</pre>"
    ), reply_markup=phone_markup)
    
    cli = Client(str(user_id), api_id=API_ID, api_hash=API_HASH)
    dic[user_id] = [cli]
    await cli.connect()

@Client.on_message(filters.private, group=watch)
async def cwf(client, message):
    user_id = message.from_user.id
    if not in_work(user_id):
        return
    if not message.text:
        return
    if message.text.startswith("/"):
        return

    lis = dic[user_id]
    if len(lis) == 1:
        cli = lis[0]
        lis.append(message.text)
        try:
            hash = await cli.send_code(message.text)
        except ConnectionError:
            await cli.connect()
            hash = await cli.send_code(message.text)
        except PhoneNumberInvalid:
            dic.pop(user_id)
            return await message.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)
        lis.append(hash.phone_code_hash)
        await message.reply("**Enter OTP:**")
    elif len(lis) == 3:
        cli = lis[0]
        txt = message.text.replace(" ", "")
        lis.append(txt)
        try:
            await cli.sign_in(lis[1], lis[2], lis[3])
            session = await cli.export_session_string()
            await update_session(user_id, session)
            await cli.disconnect()
            dic.pop(user_id)
            await message.reply("**Successfully Connected..**")
        except PhoneCodeInvalid:
            dic.pop(user_id)
            return await message.reply('**Invalid OTP!**')
        except SessionPasswordNeeded:
            await message.reply("**Enter Two Step Verification Password:**")
    elif len(lis) == 4:
        cli = lis[0]
        lis.append(message.text)
        try:
            await cli.check_password(lis[4])
            await cli.sign_in(lis[1], lis[2], lis[3])
            session = await cli.export_session_string()
            await update_session(user_id, session)
            await cli.disconnect()
            dic.pop(user_id)
            await message.reply("**Connected Successfully.**")
        except PhoneCodeInvalid:
            dic.pop(user_id)
            return await message.reply('**Invalid OTP!**')
        except PasswordHashInvalid:
            dic.pop(user_id)
            return await message.reply('**Invalid Two Step Verification Password.**')

@Client.on_message(filters.command("terminate"))
async def term(client, message):
    user_id = message.from_user.id
    if not in_work(user_id):
        return
    dic.pop(user_id)
    await message.reply("**Process Terminated.**")