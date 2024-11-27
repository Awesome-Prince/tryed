@Client.on_callback_query()
async def cbq(_, q: CallbackQuery):
    data = q.data
    if data == 'sharewithme':
        try:
            settings = await get_settings()
            await q.answer('Thank You', show_alert=True)
            new = await q.edit_message_reply_markup(reply_markup=None)
            if not settings['auto_save']:
                await new.copy(AUTO_SAVE_CHANNEL_ID)
        except Exception as e:
            logging.error(f"Error while handling 'sharewithme': {e}")
            await q.answer("Error while processing the request.", show_alert=True)
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
        try:
            new_value = await toggle_setting('auto_approval', (await get_settings())['auto_approval'])
            await q.answer()
            await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
        except Exception as e:
            logging.error(f"Error while toggling 'auto_approval': {e}")
            await q.answer("Error while toggling the setting.", show_alert=True)
    
    elif data == 'toggle_join':
        try:
            new_value = await toggle_setting('join', (await get_settings())['join'])
            await q.answer()
            await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
        except Exception as e:
            logging.error(f"Error while toggling 'join': {e}")
            await q.answer("Error while toggling the setting.", show_alert=True)
    
    elif data == 'toggle_leave':
        try:
            new_value = await toggle_setting('leave', (await get_settings())['leave'])
            await q.answer()
            await q.edit_message_reply_markup(reply_markup=markup(await get_settings()))
        except Exception as e:
            logging.error(f"Error while toggling 'leave': {e}")
            await q.answer("Error while toggling the setting.", show_alert=True)
    
    # Add more similar error handling for other settings toggles...
    
    elif data.startswith(("toggleab", "togglesu", "togglemc", "togglead", "activate")):
        try:
            await pay_cbq(_, q)
        except Exception as e:
            logging.error(f"Error while processing privilege toggle: {e}")
            await q.answer("Error while toggling privileges.", show_alert=True)
