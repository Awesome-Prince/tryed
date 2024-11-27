from Database.users import get_users_2, del_user_2
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import SUDO_USERS
import asyncio

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

@Client.on_message(filters.private & filters.command('bt') & filters.user(SUDO_USERS))
async def send_text(client, message):
    """Handles broadcasting a message to all users as a reply."""
    
    # Check if the command is a reply to another message
    if message.reply_to_message:
        query = await get_users_2()  # Fetch all user IDs
        broadcast_msg = message.reply_to_message  # Message to broadcast
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message... This will take some time.</i>")
        err = None
        
        # Iterate over all users and send the message
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)  # Try to send the message
                successful += 1
            except FloodWait as e:
                # Handle rate limits and retry
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                # Handle blocked users and remove them from the list
                await del_user_2(chat_id)
                blocked += 1
            except InputUserDeactivated:
                # Handle deactivated users and remove them from the list
                await del_user_2(chat_id)
                deleted += 1
            except Exception as e:
                # Catch other exceptions and track them
                unsuccessful += 1
                err = e  # Store the error for reporting
                pass
            total += 1
        
        # Format the status message after broadcasting
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>

Error: {err if err else 'None'}"""
        
        # Edit the waiting message with the final status
        return await pls_wait.edit(status)

    else:
        # If the command is not a reply, send an error message
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)  # Wait for a while before deleting the error message
        await msg.delete()
