from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection setup
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.mydatabase  # Adjust as per your database configuration

from time import time
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
)
from config import TUTORIAL_LINK, AUTO_DELETE_TIME
from helpers import get_chats

# Function to handle FloodWait exceptions
async def tryer(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)
