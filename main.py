from pyrogram import Client, idle
from config import Config
import sys
from resolve import ResolvePeer

# List of forced subscription channels
FSUB = [Config.FSUB1, Config.FSUB2]

class ClientLike(Client):
    """
    Custom Client class for handling additional functionality.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def resolve_peer(self, id):
        obj = ResolvePeer(self)
        return await obj.resolve_peer(id)

# Initialize the main bot client
app = ClientLike(
    'bot1',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root='Plugins')
)

# Initialize the notifier bot client
app1 = ClientLike(
    'bot2',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN2,
    plugins=dict(root='Plugins1')
)

async def start() -> None:
    """
    Start the bot clients and run initial checks.
    """
    await app.start()
    await app1.start()
    ret = False

    async def test_message(client, channel_id, channel_name) -> None:
        """
        Test if the bot can send a message to the given channel.
        """
        nonlocal ret
        try:
            message = await client.send_message(channel_id, '.')
            await message.delete()
        except Exception as e:
            print(f'Bot cannot send message in {channel_name} channel. Error: {e}')
            ret = True

    # Test message sending capability for each important channel
    await test_message(app, Config.DB_CHANNEL_ID, 'DB')
    await test_message(app, Config.DB_CHANNEL2_ID, 'Backup DB')
    await test_message(app, Config.AUTO_SAVE_CHANNEL_ID, 'Auto Save')

    if Config.LOG_CHANNEL_ID:
        await test_message(app, Config.LOG_CHANNEL_ID, 'LOG')

    # Test message sending capability for forced subscription channels
    for channel_id in FSUB:
        await test_message(app, channel_id, f'FSUB {channel_id}')
        await test_message(app1, channel_id, f'Notifier Bot FSUB {channel_id}')

    # Exit if any test failed
    if ret:
        sys.exit()

    # Print bot usernames
    bot_user = await app.get_me()
    notifier_bot_user = await app1.get_me()
    print(f'@{bot_user.username} started.')
    print(f'@{notifier_bot_user.username} started.')

    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(start())