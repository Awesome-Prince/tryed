from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the bot client
app = Client(
    ':test_bot:',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root='Plugins')
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I am testing BOT_TOKEN.")

if __name__ == "__main__":
    app.run()
