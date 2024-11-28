from pyrogram import Client
from pyrogram.types import CallbackQuery
from config import SUDO_USERS, AUTO_SAVE_CHANNEL_ID
from .settings import markup
from Database.settings import get_settings, update_settings
from .paid import pay_cbq

@Client.on_callback_query()
async def cbq_handler(client: Client, callback_query: CallbackQuery) -> None:
    """
    Handles callback queries received by the bot.
    """
    data = callback_query.data

    async def toggle_setting(setting_key: str, default_value=None):
        settings = await get_settings()
        settings[setting_key] = not settings.get(setting_key, default_value)
        mark = markup(settings)
        await update_settings(settings)
        await callback_query.edit_message_reply_markup(reply_markup=mark)

    if data == 'sharewithme':
        settings = await get_settings()
        await callback_query.answer('Thank You', show_alert=True)
        new_message = await callback_query.edit_message_reply_markup(reply_markup=None)
        if not settings.get('auto_save'):
            await new_message.copy(AUTO_SAVE_CHANNEL_ID)
        return

    elif data == 'connect':
        await callback_query.answer()
        return await callback_query.message.reply('Type /connect.')

    if callback_query.from_user.id not in SUDO_USERS:
        return await callback_query.answer()

    if data == 'answer':
        await callback_query.answer()

    elif data == 'toggle_approval':
        await toggle_setting('auto_approval')

    elif data == 'toggle_join':
        await toggle_setting('join')

    elif data == 'toggle_leave':
        await toggle_setting('leave')

    elif data == 'toggle_image':
        await toggle_setting('image')

    elif data == 'toggle_gen':
        await toggle_setting('generate', 10 if await get_settings().get('generate', 10) == 1 else 1)

    elif data == 'toggle_save':
        await toggle_setting('auto_save', False)

    elif data == 'toggle_logs':
        await toggle_setting('logs', True)

    elif data.startswith(("toggleab", "togglesu", "togglemc", "togglead", "activate")):
        await pay_cbq(client, callback_query)