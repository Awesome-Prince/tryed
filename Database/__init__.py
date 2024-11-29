from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI, DATABASE_NAME  # Import from config.py

# MongoDB connection setup with environment variable
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client[DATABASE_NAME]  # Use the database name from config

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
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            print(f"Flood wait: waiting for {e.value} seconds.")
            await asyncio.sleep(e.value + 1)  # Waiting time as suggested by Telegram

# Exporting necessary variables and functions
__all__ = ['tryer']
