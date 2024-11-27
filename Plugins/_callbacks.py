from pyrogram import Client
from pyrogram.types import CallbackQuery
from config import SUDO_USERS, AUTO_SAVE_CHANNEL_ID
from .settings import markup
from Database.settings import get_settings, update_settings
from .paid import pay_cbq

async def toggle_setting(setting: str, current_value: bool) -> bool:
    """Toggle a given setting value (True/False)."""
    new_value = not current_value
    dic = await get_settings()
    dic[setting] = new_value
    await update_settings(dic)
    return new_value

@Client.on_callback_query()
async def cbq(_, q: CallbackQuery):
    data = q.data
    if data == 'sharewithme':
        settings = await get_settings()
        await q.answer('Thank You', show_alert=True)
        new = await q.edit_message_reply_markup(reply_markup=None)
        if not settings['auto_save']:
            await new.copy(AUTO_SAVE_CHANNEL_ID)
        return
    elif data == 'connect':
        await q.answer()
        return await q.message.reply('Type /connect.')
    
    if not q.from_user.id in SUDO_USERS:
        return await q.answer()

    if data == 'answer':
        await q.answer()
    
    # Settings toggles (Refactored to use toggle_setting function)
    elif data == 'toggle_approval':
        new_value = await toggle_setting('auto_approval', (await get_settings())['auto_approval'])
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
    
    elif data == 'toggle_join':
        new_value = await toggle_setting('join', (await get_settings())['join'])
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
    
    elif data == 'toggle_leave':
        new_value = await toggle_setting('leave', (await get_settings())['leave'])
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
    
    elif data == 'toggle_image':
        new_value = await toggle_setting('image', (await get_settings())['image'])
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
    
    elif data == 'toggle_gen':
        dic = await get_settings()
        dic['generate'] = 10 if dic.get('generate', 10) == 1 else 1
        await update_settings(dic)
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(dic))
    
    elif data == "toggle_save":
        new_value = await toggle_setting('auto_save', (await get_settings()).get('auto_save', False))
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
    
    elif data == "toggle_logs":
        new_value = await toggle_setting('logs', (await get_settings()).get('logs', True))
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))

    # For activating features like ab, su, mc, ad, or activating paid users
    elif data.startswith(("toggleab", "togglesu", "togglemc", "togglead", "activate")):
        await pay_cbq(_, q)
