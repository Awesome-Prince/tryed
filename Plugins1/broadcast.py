import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import SUDO_USERS
from Database.users import get_users_2, del_user_2

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

@Client.on_message(filters.private & filters.command('bt') & filters.user(SUDO_USERS))
async def send_text(client, message):
    """
    Handles the /bt command to broadcast a message to all users.
    """
    if message.reply_to_message:
        query = await get_users_2()
        broadcast_msg = message.reply_to_message
        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        err = None
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user_2(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user_2(chat_id)
                deleted += 1
            except Exception as e:
                unsuccessful += 1
                err = e
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u></b>\n\n<b>Total Users:</b> <code>{total}</code>\n<b>Successful:</b> <code>{successful}</code>\n<b>Blocked Users:</b> <code>{blocked}</code>\n<b>Deleted Accounts:</b> <code>{deleted}</code>\n<b>Unsuccessful:</b> <code>{unsuccessful}</code>\n\n<b>Error:</b> {err}"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
