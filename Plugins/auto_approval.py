from pyrogram import Client, filters
from config import FSUB
from Database.settings import get_settings

@Client.on_chat_join_request(filters.chat(FSUB))
async def cjr(client: Client, request):
    # Fetch the settings once to avoid multiple database calls
    settings = await get_settings()
    
    # Auto approval check
    if not settings['auto_approval']:
        return
    
    try:
        # Approve the join request
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        
        # Send a welcome message to the user
        await client.send_message(request.from_user.id, "Hi")
    except Exception as e:
        # Log any error that occurs
        print(f"Error processing join request: {e}")
