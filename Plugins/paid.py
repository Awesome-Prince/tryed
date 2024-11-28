import asyncio
import datetime
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from Database.privileges import *
from Database.subscription import get_all_subs, del_sub, active_sub
from templates import SU_TEXT, EXPIRE_TEXT
from config import SUDO_USERS, EXPIRY_TIME, CONNECT_TUTORIAL_LINK, SU_IMAGE
from . import tryer
from main import app

# Calculate expiry time in seconds
exp = int(EXPIRY_TIME * 86400)

def build_markup_2(privileges, user_id, activate=True):
    """
    Build inline keyboard markup for user privileges.
    """
    return IKM(
        [
            [IKB("𝘈𝘭𝘰𝘸 𝘉𝘢𝘵𝘤𝘩", callback_data="answer"), IKB("✅" if privileges[0] else "❌", callback_data=f"toggleab_{user_id}")],
            [IKB("𝘚𝘶𝘱𝘦𝘳 𝘜𝘴𝘦𝘳", callback_data="answer"), IKB("✅" if privileges[1] else "❌", callback_data=f"togglesu_{user_id}")],
            [IKB("𝘔𝘺 𝘤𝘰𝘯𝘵𝘦𝘯𝘵", callback_data="answer"), IKB("✅" if privileges[2] else "❌", callback_data=f"togglemc_{user_id}")],
            [IKB("𝘈𝘭𝘭𝘰𝘸 𝘋𝘔", callback_data="answer"), IKB("✅" if privileges[3] else "❌", callback_data=f"togglead_{user_id}")],
            [IKB("𝘈𝘤𝘵𝘪𝘷𝘢𝘵𝘦" if activate else "𝘋𝘦𝘢𝘤𝘵𝘪𝘷𝘢𝘵𝘦", callback_data=f"activate_{user_id}")]
        ]
    )

@Client.on_message(filters.command("super") & filters.user(SUDO_USERS) & filters.private)
async def pay_settings(client: Client, message: Message):
    """
    Handle the /super command to manage user privileges and subscriptions.
    """
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        return await message.reply("**Usage:** `/super [ID]`")
    
    privileges = await get_privileges(user_id)
    subs = await get_all_subs()
    
    if user_id in subs:
        elapsed_time = int(time.time() - subs[user_id])
        remaining_time = exp - elapsed_time
        expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=remaining_time)
        await message.reply(
            f"**This User Already SuperUser**\n<pre>Expiry: {expiry_date.day}-{expiry_date.month}-{expiry_date.year}</pre>", 
            reply_markup=build_markup_2(privileges, user_id, activate=False)
        )
    else:
        await message.reply("**Before Activate Give Access..**", reply_markup=build_markup_2(privileges, user_id))

me = None
async def activate_cbq(client: Client, callback_query: CallbackQuery):
    """
    Handle the callback query to activate or deactivate a user subscription.
    """
    global me
    if not me:
        me = await client.get_me()
    
    user_id = int(callback_query.data.split("_")[1])
    privileges = await get_privileges(user_id)
    subs = await get_all_subs()
    
    if user_id not in subs:
        can_activate = any(privileges)
        if not can_activate:
            return await callback_query.answer("At least one privilege should be up to activate.", show_alert=True)
        
        markup = None
        if privileges[1]:
            markup = IKM([[IKB("𝘊𝘰𝘯𝘯𝘦𝘤𝘵", callback_data='connect'), IKB("𝘛𝘶𝘵𝘰𝘳𝘪𝘢𝘭", url=CONNECT_TUTORIAL_LINK)]])
        
        await active_sub(user_id)
        expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=exp)
        
        await tryer(
            client.send_photo, 
            user_id, 
            SU_IMAGE, 
            caption=SU_TEXT.format((await client.get_users(user_id)).mention, f'{expiry_date.day}-{expiry_date.month}-{expiry_date.year}'), 
            reply_markup=markup
        )
        await callback_query.answer()
        await tryer(callback_query.edit_message_text, 'Activated.', reply_markup=None)
    else:
        can_deactivate = not any(privileges)
        if not can_deactivate:
            return await callback_query.answer("Disable all privileges to deactivate.", show_alert=True)
        
        await del_sub(user_id)
        markup = IKM([[IKB('𝘛𝘢𝘭𝘬 𝘛𝘰 𝘈𝘥𝘮𝘪𝘯', url='https://t.me/CuteGirlTG?text=%2A%2A%20I%20saw%20my%20subscription%20is%20stopped%20by%20admin%20but%20why%3F%20%2A%2A')]])
        
        await tryer(client.send_message, user_id, '**Your Membership Cancelled By Admin**', reply_markup=markup)
        await callback_query.answer()
        await tryer(callback_query.edit_message_text, 'Deactivated.', reply_markup=None)

async def pay_cbq(client: Client, callback_query: CallbackQuery):
    """
    Handle the callback query to toggle user privileges.
    """
    user_id = int(callback_query.data.split("_")[1])
    privileges = await get_privileges(user_id)
    subs = await get_all_subs()
    is_subscribed = user_id in subs
    
    if callback_query.data.startswith("toggleab"):
        privileges[0] = not privileges[0]
    elif callback_query.data.startswith("togglesu"):
        privileges[1] = not privileges[1]
    elif callback_query.data.startswith("togglemc"):
        privileges[2] = not privileges[2]
    elif callback_query.data.startswith("togglead"):
        privileges[3] = not privileges[3]
    elif callback_query.data.startswith('activate'):
        return await activate_cbq(client, callback_query)
    
    await update_privileges(user_id, privileges[0], privileges[1], privileges[2], privileges[3])
    await callback_query.answer()
    await callback_query.edit_message_reply_markup(reply_markup=build_markup_2(privileges, user_id, activate=not is_subscribed)) 

# Inline keyboard markup for renewal
renew = IKM([[IKB("𝘉𝘶𝘺 𝘈𝘨𝘢𝘪𝘯", url="https://t.me/CuteGirlTG?text=**Hii%20I%20Want%20To%20Renew%20My%20Membership...**")]])

async def task():
    """
    Periodically check for expired subscriptions and handle deactivation.
    """
    while True:
        subs = await get_all_subs()
        for user_id in subs:
            if int(time.time() - subs[user_id]) >= exp:
                await del_sub(user_id)
                await update_privileges(user_id, False, False, False, False) 
                mention = (await tryer(app.get_users, user_id)).mention
                await tryer(app.send_photo, user_id, SU_IMAGE, caption=EXPIRE_TEXT.format(mention, mention), reply_markup=renew)
        await asyncio.sleep(exp / 1000)
        
asyncio.create_task(task())