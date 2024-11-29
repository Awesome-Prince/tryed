from pyrogram import Client, filters
from config import FSUB_1, FSUB_2
from Database.settings import get_settings
from Database import tryer
import asyncio 

@Client.on_chat_join_request(filters.chat([FSUB_1, FSUB_2]))
async def cjr(client: Client, request):
    """
    Automatically approve chat join requests if auto-approval is enabled.
    """
    settings = await get_settings()
    if not settings['auto_approval']:
        return

    # Add delay before approving the request
    await asyncio.sleep(1)  
    
    # Approve the chat join request
    await tryer(client.approve_chat_join_request, request.chat.id, request.from_user.id)

    # Add delay before sending the welcome message
    await asyncio.sleep(1)  

    # Send a welcome message to the user
    await tryer(client.send_message, request.from_user.id, "Hi")
