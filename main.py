from pyrogram import Client, idle
from config import *
import sys
from resolve import ResolvePeer
import asyncio
from time import time

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

async def start():
    await app.start()
    await app1.start()
    ret = False

    async def send_and_delete(client, channel_id, message):
        try:
            await client.rate_limit(channel_id, delay=0.5)  # Reduced delay for better performance
            m = await client.send_message(channel_id, message)
            await m.delete()
        except Exception as e:
            print(e)
            return False
        return True

    tasks = [
        send_and_delete(app, DB_CHANNEL_ID, '.'),
        send_and_delete(app, DB_CHANNEL_2_ID, '.'),
        send_and_delete(app, AUTO_SAVE_CHANNEL_ID, '.')
    ]
    if LOG_CHANNEL_ID:
        tasks.append(send_and_delete(app, LOG_CHANNEL_ID, '.'))

    for x in FSUB:
        tasks.append(send_and_delete(app, x, '.'))
        tasks.append(send_and_delete(app1, x, '.'))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    if any(not result for result in results):
        sys.exit()

    x = await app.get_me()
    y = await app1.get_me()
    print(f'@{x.username} started.')
    print(f'@{y.username} started.')
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
