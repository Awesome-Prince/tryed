from pyrogram import Client, filters
from config import SUDO_USERS
from Database.users import add_user_2

watch = 69

@Client.on_message(filters.private, group=watch)
async def cwf(client: Client, message: Message):
    """
    Handle incoming private messages and add the user to the database.
    """
    if message.from_user and message.from_user.id in SUDO_USERS:
        return await add_user_2(message.from_user.id)
    await message.reply("**Message Me Here @CuteGirlTG**")
    await add_user_2(message.from_user.id)