from Database.settings import *
from pyrogram import Client, filters
from config import SUDO_USERS
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from time import time
import asyncio

# Constants for toggle values
YES = '☑️'
NO = '❌'

# Function to create the markup with dynamic values
def markup(dic):
    mark = IKM(
        [
            [
                IKB('𝘈𝘶𝘵𝘰 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭', callback_data='answer'),
                IKB(YES if dic.get('auto_approval', True) else NO, callback_data='toggle_approval')
            ],
            [
                IKB('𝘞𝘦𝘭𝘤𝘰𝘮𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(YES if dic.get('join', True) else NO, callback_data='toggle_join')
            ],
            [
                IKB('𝘓𝘦𝘢𝘷𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(YES if dic.get('leave', True) else NO, callback_data='toggle_leave')
            ],
            [
                IKB('𝘞𝘢𝘯𝘵 𝘐𝘮𝘢𝘨𝘦', callback_data='answer'),
                IKB(YES if dic.get('image', True) else NO, callback_data='toggle_image')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘚𝘢𝘷𝘦', callback_data='answer'),
                IKB(YES if dic.get('auto_save', True) else NO, callback_data='toggle_save')
            ],
            [
                IKB('𝘓𝘰𝘨 𝘊𝘩𝘢𝘯𝘯𝘦𝘭', callback_data='answer'),
                IKB(YES if dic.get('logs', True) else NO, callback_data='toggle_logs')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦', callback_data='answer'),
                IKB(dic.get('generate', 10), callback_data='toggle_gen')
            ]
        ]
    )
    return mark

# Store user interactions for timeout check
dic = {}

# Command handler to show settings and allow modification
@Client.on_message(filters.command('settings') & filters.user(SUDO_USERS))
async def settings(_, m):
    set = await get_settings()
    txt = '**IT Helps To Change Bot Basic Settings..**'
    mark = markup(set)
    ok = await m.reply(txt, reply_markup=mark)
    dic[m.from_user.id] = [ok, time()]

# Background task to delete old messages
async def task():
    while True:
        rem = []
        for x in dic:
            if int(time() - dic[x][1]) > 120:  # Timeout after 120 seconds
                try:
                    await dic[x][0].delete()  # Delete message
                except Exception as e:
                    print(f"Error deleting message: {e}")  # Log the error
                rem.append(x)
        # Remove timed-out users from dictionary
        for y in rem:
            del dic[y]
        await asyncio.sleep(1)

# Start the background task
asyncio.create_task(task())
