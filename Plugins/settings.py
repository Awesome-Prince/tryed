from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import SUDO_USERS
from Database.settings import get_settings
from time import time
import asyncio

# Constants for Yes and No symbols
yes = '☑️'
no = '❌'

# Function to create the settings markup
def markup(settings_dict):
    return IKM(
        [
            [
                IKB('𝘈𝘶𝘵𝘰 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭', callback_data='answer'),
                IKB(yes if settings_dict.get('auto_approval', True) else no, callback_data='toggle_approval')
            ],
            [
                IKB('𝘞𝘦𝘭𝘤𝘰𝘮𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if settings_dict.get('join', True) else no, callback_data='toggle_join')
            ],
            [
                IKB('𝘓𝘦𝘢𝘷𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if settings_dict.get('leave', True) else no, callback_data='toggle_leave')
            ],
            [
                IKB('𝘞𝘢𝘯𝘵 𝘐𝘮𝘢𝘨𝘦', callback_data='answer'),
                IKB(yes if settings_dict.get('image', True) else no, callback_data='toggle_image')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘚𝘢𝘷𝘦', callback_data='answer'),
                IKB(yes if settings_dict.get('auto_save', True) else no, callback_data='toggle_save')
            ],
            [
                IKB('𝘓𝘰𝘨 𝘊𝘩𝘢𝘯𝘯𝘦𝘭', callback_data='answer'),
                IKB(yes if settings_dict.get('logs', True) else no, callback_data='toggle_logs')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦', callback_data='answer'),
                IKB(str(settings_dict.get('generate', 10)), callback_data='toggle_gen')
            ]
        ]
    )

# Dictionary to store user-specific settings message and timestamp
user_settings = {}

@Client.on_message(filters.command('settings') & filters.user(SUDO_USERS))
async def settings(_, m):
    settings_dict = await get_settings()
    txt = '**IT Helps To Change Bot Basic Settings..**'
    mark = markup(settings_dict)
    settings_message = await m.reply(txt, reply_markup=mark)
    user_settings[m.from_user.id] = [settings_message, time()]

async def cleanup_task():
    while True:
        to_remove = []
        for user_id, (msg, timestamp) in user_settings.items():
            if int(time() - timestamp) > 120:
                try:
                    await msg.delete()
                except:
                    pass
                to_remove.append(user_id)
        for user_id in to_remove:
            del user_settings[user_id]
        await asyncio.sleep(1)
        
asyncio.create_task(cleanup_task())
