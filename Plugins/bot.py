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

# Inline keyboard markup for the phone number shortcut button
phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘤𝘶𝘵', url='tg://settings')]])

# Dictionary to track ongoing connection processes
ongoing_connections = {}
watch_group = 69

def is_in_work(user_id):
    return user_id in ongoing_connections

@Client.on_message(filters.command('connect') & filters.private)
async def connect_handler(client, message):
    user_id = message.from_user.id
    privileges = await get_privileges(user_id)
    if not privileges[1]:
        return await tryer(message.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(client))
    
    session = await get_session(user_id)
    if session:
        app = Client(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        try:
            await app.start()
            await message.reply("**You Are Already Connected User**")
            await app.stop()
            return
        except:
            await del_session(user_id)
    
    if is_in_work(user_id):
        return await message.reply("**Process Ongoing..., use /terminate to cancel.**")
    
    await message.reply_photo(PHONE_NUMBER_IMAGE, caption=(
        "**Enter Your Phone Number With Country Code.\n"
        "<pre>How To Find Number?</pre>\n"
        "You can Use Shortcut Button To Find Your Number\n"
        "<pre>Incase Shortcut Button Not Working Then You Need To Find Manually</pre>"
    ), reply_markup=phone_markup)
    
    client_instance = Client(str(user_id), api_id=API_ID, api_hash=API_HASH)
    ongoing_connections[user_id] = [client_instance]
    await client_instance.connect()

@Client.on_message(filters.private, group=watch_group)
async def continue_workflow_handler(client, message):
    user_id = message.from_user.id
    if not is_in_work(user_id):
        return
    if not message.text or message.text.startswith("/"):
        return

    workflow_data = ongoing_connections[user_id]
    if len(workflow_data) == 1:
        client_instance = workflow_data[0]
        workflow_data.append(message.text)
        try:
            code_hash = await client_instance.send_code(message.text)
        except ConnectionError:
            await client_instance.connect()
            code_hash = await client_instance.send_code(message.text)
        except PhoneNumberInvalid:
            ongoing_connections.pop(user_id)
            return await message.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)
        workflow_data.append(code_hash.phone_code_hash)
        await message.reply("**Enter OTP:**")
    elif len(workflow_data) == 3:
        client_instance = workflow_data[0]
        otp_code = message.text.replace(" ", "")
        workflow_data.append(otp_code)
        try:
            await client_instance.sign_in(workflow_data[1], workflow_data[2], workflow_data[3])
            session_string = await client_instance.export_session_string()
            await update_session(user_id, session_string)
            await client_instance.disconnect()
            ongoing_connections.pop(user_id)
            await message.reply("**Successfully Connected..**")
        except PhoneCodeInvalid:
            ongoing_connections.pop(user_id)
            return await message.reply('**Invalid OTP!**')
        except SessionPasswordNeeded:
            await message.reply("**Enter Two Step Verification Password:**")
    elif len(workflow_data) == 4:
        client_instance = workflow_data[0]
        workflow_data.append(message.text)
        try:
            await client_instance.check_password(workflow_data[4])
            await client_instance.sign_in(workflow_data[1], workflow_data[2], workflow_data[3])
            session_string = await client_instance.export_session_string()
            await update_session(user_id, session_string)
            await client_instance.disconnect()
            ongoing_connections.pop(user_id)
            await message.reply("**Connected Successfully.**")
        except PhoneCodeInvalid:
            ongoing_connections.pop(user_id)
            return await message.reply('**Invalid OTP!**')
        except PasswordHashInvalid:
            ongoing_connections.pop(user_id)
            return await message.reply('**Invalid Two Step Verification Password.**')

@Client.on_message(filters.command("terminate"))
async def terminate_handler(client, message):
    user_id = message.from_user.id
    if not is_in_work(user_id):
        return
    ongoing_connections.pop(user_id)
    await message.reply("**Process Terminated.**")