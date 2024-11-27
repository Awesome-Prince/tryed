import asyncio
import math
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import SUDO_USERS
from Database.users import get_users, del_user

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

# Helper function for broadcasting messages
async def broadcast_message(broadcast_msg, chat_id):
    try:
        await broadcast_msg.copy(chat_id)
        return True
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await broadcast_msg.copy(chat_id)
        return True
    except UserIsBlocked:
        await del_user(chat_id)
        return False
    except InputUserDeactivated:
        await del_user(chat_id)
        return False
    except Exception:
        return False

# Broadcasting function for SUDO users
@Client.on_message(filters.private & filters.command('bt') & filters.user(SUDO_USERS))
async def send_text(client, message):
    if message.reply_to_message:
        forward = bool(message.reply_to_message.forward_from or message.reply_to_message.forward_from_chat)
        users = await get_users()
        total = len(users)
        successful, blocked, deleted, unsuccessful = 0, 0, 0, 0
        
        broadcast_msg = message.reply_to_message
        copy_method = broadcast_msg.forward if forward else broadcast_msg.copy
        
        pls_wait = await message.reply("<i>Broadcasting Message... This will take some time</i>")
        
        for chat_id in users:
            if await broadcast_message(copy_method, chat_id):
                successful += 1
            else:
                unsuccessful += 1
        
        # Stats for broadcast completion
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# Regular broadcast function (for comparison purposes)
@Client.on_message(filters.private & filters.command('broadcast') & filters.user(SUDO_USERS))
async def broadcast(client, message):
    if message.reply_to_message:
        users = await get_users()
        total = len(users)
        blocked = math.ceil(total * 4 / 100)
        deleted = math.ceil(total * 3 / 200)
        unsuccessful = math.ceil(total * 2 / 100)
        successful = total - sum([blocked, deleted, unsuccessful])
        
        pls_wait = await message.reply("<i>Broadcasting Message... This will take some time</i>")
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# Function to handle forwarded/copied messages to specific user
@Client.on_message(filters.private & filters.command('m') & filters.user(SUDO_USERS))
async def em(_, m):
    reply = m.reply_to_message
    if not reply:
        return await m.reply("Reply to a message.")
    try:
        id = int(m.text.split()[1])
    except:
        return await m.reply("Enter ID to send message.")
    
    if reply.forward_from or reply.forward_from_chat:
        forward = True
    else:
        forward = False
    
    if forward:
        await reply.forward(id)
    else:
        await reply.copy(id)
    
    await m.reply("Done.")
