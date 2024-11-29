from config import FSUB_1, FSUB_2  # Importing from config
import asyncio
import logging
from pyrogram.errors import FloodWait

# Setup logging for better debugging and production tracking
logging.basicConfig(level=logging.INFO)

chats = []  # Define and initialize the global variable

async def tryer(func, *args, **kwargs):
    """
    Function to handle FloodWait exceptions and retry after wait time.
    """
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            logging.warning(f"Flood wait: waiting for {e.value} seconds.")
            await asyncio.sleep(e.value + 1)  # Waiting time as suggested by Telegram

async def get_chats(client):
    """
    Get the subscription channels and generate invite links.
    Fetches chat details and generates the invite link for each.
    """
    global chats
    if not chats:
        try:
            # Use asyncio.gather to fetch all chats concurrently
            chat_results = await asyncio.gather(
                client.get_chat(FSUB_1),
                client.get_chat(FSUB_2)
            )
            chats = chat_results

            # Log chat details for verification
            logging.info(f"Fetched chats: {chats}")

            # Use asyncio.gather for invite link generation in parallel
            new_links = await asyncio.gather(
                *[client.create_chat_invite_link(chat.id, creates_join_request=True) for chat in chats]
            )
            for idx, chat in enumerate(chats):
                chat.invite_link = new_links[idx].invite_link  # Assign the invite link to the chat object

            # Log the generated invite links
            logging.info(f"Generated invite links: {[chat.invite_link for chat in chats]}")

        except Exception as e:
            logging.error(f"Error in get_chats function: {e}")
            return None  # Properly handle errors to avoid NoneType issues

    return chats

# Exporting necessary functions and variables
__all__ = ['get_chats', 'tryer']
