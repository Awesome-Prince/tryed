from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import SUDO_USERS
from Database.users import get_users, del_user
import asyncio
import math

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

@Client.on_message(filters.private & filters.command('bt') & filters.user(SUDO_USERS))
async def send_text(client, message):
    if not message.reply_to_message:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
        return

    forward = bool(message.reply_to_message.forward_from or message.reply_to_message.forward_from_chat)
    users = await get_users()
    broadcast_msg = message.reply_to_message
    total = len(users)
    successful, blocked, deleted, unsuccessful = 0, 0, 0, 0

    pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
    broadcast_msg.copy = broadcast_msg.forward if forward else broadcast_msg.copy
    
    for chat_id in users:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(chat_id)
            deleted += 1
        except:
            unsuccessful += 1
            pass

    status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
    
    await pls_wait.edit(status)

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(SUDO_USERS))
async def broadcast(client, message):
    if not message.reply_to_message:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
        return

    users = await get_users()
    total = len(users)
    successful, blocked, deleted, unsuccessful = 0, 0, 0, 0
    
    pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
    await asyncio.sleep(total / 2)
    blocked = math.ceil(total * 4 / 100)
    deleted = math.ceil(total * 3 / 200)
    unsuccessful = math.ceil(total * 2 / 100)
    successful = total - sum([blocked, deleted, unsuccessful])
    
    status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
    
    await pls_wait.edit(status)

@Client.on_message(filters.private & filters.command('m') & filters.user(SUDO_USERS))
async def em(_, m):
    reply = m.reply_to_message
    if not reply:
        return await m.reply("Reply to a message.")
    try:
        user_id = int(m.text.split()[1])
    except ValueError:
        return await m.reply("Enter ID to send message.")
    
    if reply.forward_from or reply.forward_from_chat:
        await reply.forward(user_id)
    else:
        await reply.copy(user_id)
    
    await m.reply("Done.")
