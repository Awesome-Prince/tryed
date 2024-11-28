import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import SUDO_USERS
from Database.settings import get_settings

# Symbols for yes and no
yes = '☑️'
no = '❌'

def markup(settings: dict) -> IKM:
    """
    Generate an inline keyboard markup for bot settings.
    """
    return IKM(
        [
            [
                IKB('𝘈𝘶𝘵𝘰 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭', callback_data='answer'),
                IKB(yes if settings.get('auto_approval', True) else no, callback_data='toggle_approval')
            ],
            [
                IKB('𝘞𝘦𝘭𝘤𝘰𝘮𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if settings.get('join', True) else no, callback_data='toggle_join')
            ],
            [
                IKB('𝘓𝘦𝘢𝘷𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if settings.get('leave', True) else no, callback_data='toggle_leave')
            ],
            [
                IKB('𝘞𝘢𝘯𝘵 𝘐𝘮𝘢𝘨𝘦', callback_data='answer'),
                IKB(yes if settings.get('image', True) else no, callback_data='toggle_image')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘚𝘢𝘷𝘦', callback_data='answer'),
                IKB(yes if settings.get('auto_save', True) else no, callback_data='toggle_save')
            ],
            [
                IKB('𝘓𝘰𝘨 𝘊𝘩𝘢𝘯𝘯𝘦𝘭', callback_data='answer'),
                IKB(yes if settings.get('logs', True) else no, callback_data='toggle_logs')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦', callback_data='answer'),
                IKB(str(settings.get('generate', 10)), callback_data='toggle_gen')
            ]
        ]
    )

# Dictionary to keep track of messages
dic = {}

@Client.on_message(filters.command('settings') & filters.user(SUDO_USERS))
async def settings(client: Client, message: Message):
    """
    Display bot settings and provide options to change them.
    """
    current_settings = await get_settings()
    text = '**IT Helps To Change Bot Basic Settings..**'
    mark = markup(current_settings)
    reply_msg = await message.reply(text, reply_markup=mark)
    dic[message.from_user.id] = [reply_msg, time()]

async def task():
    """
    Periodically remove settings messages that have been inactive for over 2 minutes.
    """
    while True:
        to_remove = []
        for user_id in dic:
            if int(time() - dic[user_id][1]) > 120:
                try:
                    await dic[user_id][0].delete()
                except Exception:
                    pass
                to_remove.append(user_id)
        for user_id in to_remove:
            del dic[user_id]
        await asyncio.sleep(1)
        
asyncio.create_task(task())