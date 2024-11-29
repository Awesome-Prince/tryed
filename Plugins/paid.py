from config import SUDO_USERS, EXPIRY_TIME, CONNECT_TUTORIAL_LINK, SU_IMAGE
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from pyrogram.errors import FloodWait
from Database.privileges import get_privileges, update_privileges
from Database.subscription import get_all_subs, del_sub, active_sub
from templates import SU_TEXT, EXPIRE_TEXT
from Database import tryer
import datetime
import asyncio
import time
from main import app

exp = int(EXPIRY_TIME * 86400)

def build_markup_2(privileges, user_id, activate=True):
    return IKM(
        [
            [IKB("Allow Batch", callback_data="answer"), IKB("✅" if privileges[0] else "❌", callback_data=f"toggleab_{user_id}")],
            [IKB("Super User", callback_data="answer"), IKB("✅" if privileges[1] else "❌", callback_data=f"togglesu_{user_id}")],
            [IKB("My Content", callback_data="answer"), IKB("✅" if privileges[2] else "❌", callback_data=f"togglemc_{user_id}")],
            [IKB("Allow DM", callback_data="answer"), IKB("✅" if privileges[3] else "❌", callback_data=f"togglead_{user_id}")],
            [IKB("Activate" if activate else "Deactivate", callback_data=f"activate_{user_id}")]
        ]
    )

@Client.on_message(filters.command("super") & filters.user(SUDO_USERS) & filters.private)
async def pay_settings(_, m):
    try:
        user_id = int(m.text.split()[1])
    except ValueError:
        return await m.reply("**Usage:** `/super [ID]`")
    
    priv = await get_privileges(user_id)
    subs = await get_all_subs()
    
    if user_id in subs:
        elapsed_seconds = int(time.time() - subs[user_id])
        remaining_seconds = exp - elapsed_seconds
        expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=remaining_seconds)
        await m.reply(f"**This User Already SuperUser**\n<pre>Expiry: {expiry_date.day}-{expiry_date.month}-{expiry_date.year}</pre>", 
                      reply_markup=build_markup_2(priv, user_id, activate=False))
    else:
        await m.reply("**Before Activate Give Access..**", reply_markup=build_markup_2(priv, user_id))

async def activate_cbq(_, q):
    global me
    if not me:
        me = await _.get_me()
    
    user_id = int(q.data.split("_")[1])
    priv = await get_privileges(user_id)
    subs = await get_all_subs()
    
    if user_id not in subs:
        if not any(priv):
            return await q.answer("At least one privilege should be up to activate.", show_alert=True)
        
        markup = IKM([[IKB("Connect", callback_data='connect'), IKB("Tutorial", url=CONNECT_TUTORIAL_LINK)]]) if priv[1] else None
        await active_sub(user_id)
        
        expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=exp)
        await tryer_with_retry(_.send_photo, user_id, SU_IMAGE, caption=SU_TEXT.format((await _.get_users(user_id)).mention, 
                                                                           f'{expiry_date.day}-{expiry_date.month}-{expiry_date-year}'), 
                                                                           reply_markup=markup)
        await q.answer()
        await asyncio.sleep(0.5)  # Minimal delay to avoid flood wait
        await tryer_with_retry(q.edit_message_text, 'Activated.', reply_markup=None)
    else:
        if any(priv):
            return await q.answer("Disable all privileges to deactivate.", show_alert=True)
        
        await del_sub(user_id)
        admin_contact_link = "https://t.me/CuteGirlTG?text=I%20saw%20my%20subscription%20is%20stopped%20by%20admin%20but%20why%3F"
        markup = IKM([[IKB('Talk To Admin', url=admin_contact_link)]])
        await tryer_with_retry(_.send_message, user_id, '**Your Membership Cancelled By Admin**', reply_markup=markup)
        await q.answer()
        await asyncio.sleep(0.5)  # Minimal delay to avoid flood wait
        await tryer_with_retry(q.edit_message_text, 'Deactivated.', reply_markup=None)

async def pay_cbq(_, q):
    user_id = int(q.data.split("_")[1])
    priv = await get_privileges(user_id)
    subs = await get_all_subs()
    
    if q.data.startswith("toggleab"):
        priv[0] = not priv[0]
    elif q.data.startswith("togglesu"):
        priv[1] = not priv[1]
    elif q.data.startswith("togglemc"):
        priv[2] = not priv[2]
    elif q.data.startswith("togglead"):
        priv[3] = not priv[3]
    elif q.data.startswith('activate'):
        return await activate_cbq(_, q)
    
    await update_privileges(user_id, priv[0], priv[1], priv[2], priv[3])
    await q.answer()
    await asyncio.sleep(0.5)  # Minimal delay to avoid flood wait
    await q.edit_message_reply_markup(reply_markup=build_markup_2(priv, user_id, activate=user_id not in subs)) 

renew = IKM([[IKB("Buy Again", url="https://t.me/CuteGirlTG?text=Hii%20I%20Want%20To%20Renew%20My%20Membership...")]])

async def task():
    while True:
        subs = await get_all_subs()
        for user_id in subs:
            if int(time.time() - subs[user_id]) >= exp:
                await del_sub(user_id)
                await update_privileges(user_id, False, False, False, False) 
                mention = (await tryer_with_retry(app.get_users, user_id)).mention
                await asyncio.sleep(0.5)  # Minimal delay to avoid flood wait
                await tryer_with_retry(app.send_photo, user_id, SU_IMAGE, caption=EXPIRE_TEXT.format(mention, mention), reply_markup=renew)
        await asyncio.sleep(exp / 1000)

asyncio.create_task(task())

async def tryer_with_retry(func, *args, **kwargs):
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)  # Wait for the specified time plus 1 second
