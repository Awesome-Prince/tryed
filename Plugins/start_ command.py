from pyrogram import Client, filters
from templates import LINK_GEN, USELESS_MESSAGE  # Import the templates

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I am your second bot.")
    
@Client.on_message(filters.command("generate_link"))
async def generate_link(client, message):
    # Use a template from templates.py
    episode_info = "Episode Information"
    bot_link = "http://example.com/bot_link"
    response = LINK_GEN.format("Episode 2", "Description", bot_link)
    await message.reply(response)
