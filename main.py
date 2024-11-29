from pyrogram import Client, idle
from config import *
import sys
import logging
from resolve import ResolvePeer
import asyncio
from time import time

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# List of channels to subscribe
FSUB = [FSUB_1, FSUB_2]

class ClientLike(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_message_time = {}

    async def resolve_peer(self, id):
        obj = ResolvePeer(self)
        return await obj.resolve_peer(id)

    async def rate_limit(self, chat_id, delay=1):
        """
        Ensure there's a delay between sending messages to avoid flood limits.
        """
        now = time()
        if chat_id in self.last_message_time:
            elapsed = now - self.last_message_time[chat_id]
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)
        self.last_message_time[chat_id] = now

# Initialize the bot clients
app = ClientLike(
    ':91:',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root='Plugins')
)

app1 = ClientLike(
    ':91-1:',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN_2,
    plugins=dict(root='Plugins1')
)

async def start_bot(bot, name):
    await bot.start()
    x = await bot.get_me()
    print(f'@{x.username} ({name}) started.')

async def start():
    try:
        # Start the first bot
        await start_bot(app, "BOT_TOKEN")
          # Delay to ensure the first bot starts properly
        
        # Start the second bot
        await start_bot(app1, "BOT_TOKEN_2")
        
        await idle()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
