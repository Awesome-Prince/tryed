from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PasswordHashInvalid
)
from Database.sessions import *
from Database.privileges import get_privileges
from config import API_ID, API_HASH, USELESS_IMAGE, PHONE_NUMBER_IMAGE
from . import build, tryer
from templates import USELESS_MESSAGE

# Inline keyboard markup for phone number shortcut
phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘤𝘶𝘵', url='tg://settings')]])

# Dictionary to track ongoing processes
dic = {}
watch = 69

def in_work(user_id: int) -> bool:
    """
    Check if a user is in the middle of a process.
    """
    return user_id in dic

@Client.on_message(filters.command('connect') & filters.private)
async def conn(client: Client, message: Message):
    """
    Start the connection process for a user.
    """
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

    await message.reply_photo(
        PHONE_NUMBER_IMAGE,
        caption=(
            "**Enter Your Phone Number With Country Code. \n"
            "<pre>How To Find Number?</pre> \n"
            "You can Use Shortcut Button To Find Your Number ** \n"
            "<pre>Incase Shortcut Button Not Working Then You Need To Find Manually</pre>"
        ),
        reply_markup=phone_markup
    )

    cli = Client(str(user_id), api_id=API_ID, api_hash=API_HASH)
    dic[user_id] = [cli]
    await cli.connect()

@Client.on_message(filters.private, group=watch)
async def cwf(client: Client, message: Message):
    """
    Handle the connection workflow.
    """
    user_id = message.from_user.id
    if not in_work(user_id):
        return
    if not message.text or message.text.startswith("/"):
        return

    steps = dic[user_id]
    if len(steps) == 1:
        cli = steps[0]
        steps.append(message.text)
        try:
            hash = await cli.send_code(message.text)
        except ConnectionError:
            await cli.connect()
            hash = await cli.send_code(message.text)
        except PhoneNumberInvalid:
            dic.pop(user_id)
            return await message.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)

        steps.append(hash.phone_code_hash)
        await message.reply("**Enter OTP:**")
        dic[user_id] = steps

    elif len(steps) == 3:
        cli = steps[0]
        otp = message.text.replace(" ", "") if " " in message.text else message.text
        steps.append(otp)
        dic[user_id] = steps

        try:
            await cli.sign_in(steps[1], steps[2], steps[3])
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

    elif len(steps) == 4:
        cli = steps[0]
        steps.append(message.text)
        dic[user_id] = steps

        try:
            await cli.check_password(steps[4])
            await cli.sign_in(steps[1], steps[2], steps[3])
        except PhoneCodeInvalid:
            dic.pop(user_id)
            return await message.reply('**Invalid OTP!**')
        except PasswordHashInvalid:
            dic.pop(user_id)
            return await message.reply('**Invalid Two Step Verification Password.**')

        session = await cli.export_session_string()
        await update_session(user_id, session)
        await cli.disconnect()
        dic.pop(user_id)
        await message.reply("**Connected Successfully.**")

@Client.on_message(filters.command("terminate"))
async def term(client: Client, message: Message):
    """
    Terminate the ongoing connection process for a user.
    """
    user_id = message.from_user.id
    if not in_work(user_id):
        return
    dic.pop(user_id)
    await message.reply("**Process Terminated.**")