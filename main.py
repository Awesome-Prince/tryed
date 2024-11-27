import sys
from pyrogram import Client, idle
from config import *
from resolve import ResolvePeer

# Subscription Channels
FSUB = [FSUB_1, FSUB_2]

# --- Custom Client Class ---
class ClientLike(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def resolve_peer(self, id):
        resolver = ResolvePeer(self)
        return await resolver.resolve_peer(id)

# --- Initialize Clients ---
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

# --- Start Function ---
async def start():
    await app.start()
    await app1.start()

    # Helper function to check channel messaging
    async def check_channel_messaging(client, channel_id, bot_name):
        try:
            message = await client.send_message(channel_id, '.')
            await message.delete()
        except Exception as e:
            print(f"{bot_name} cannot send messages to channel ID {channel_id}.")
            print(e)
            return True
        return False

    # Validate messaging for required channels
    ret = False
    channels = {
        "DB Channel": DB_CHANNEL_ID,
        "Backup DB Channel": DB_CHANNEL_2_ID,
        "Auto Save Channel": AUTO_SAVE_CHANNEL_ID,
        "Log Channel": LOG_CHANNEL_ID,
    }

    for name, channel_id in channels.items():
        if channel_id:
            ret |= await check_channel_messaging(app, channel_id, "Main Bot")

    # Check FSUB channels for both bots
    for channel_id in FSUB:
        ret |= await check_channel_messaging(app, channel_id, "Main Bot")
        ret |= await check_channel_messaging(app1, channel_id, "Notifier Bot")

    # Exit if any messaging check fails
    if ret:
        sys.exit()

    # Display bot usernames
    bot1 = await app.get_me()
    bot2 = await app1.get_me()
    print(f"@{bot1.username} started.")
    print(f"@{bot2.username} started.")

    # Keep the bot running
    await idle()
