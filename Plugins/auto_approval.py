from pyrogram import Client, filters
from config import Config
from Database.settings import get_settings

@Client.on_chat_join_request(filters.chat(Config.FSUB1, Config.FSUB2))
async def auto_approve(client: Client, request):
    # Check if auto-approval is enabled in the settings
    settings = await get_settings()
    if not settings.get('auto_approval', False):
        return

    # Approve the join request
    await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    # Send a welcome message
    await client.send_message(request.from_user.id, "Hi")