# helpers.py
import asyncio
from pyrogram.errors import FloodWait

async def tryer(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
