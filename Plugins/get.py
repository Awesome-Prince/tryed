async def send_message_with_media(_, m, msg, markup):
    if msg.text:
        return await m.reply(msg.text, reply_markup=markup)
    try:
        dl = await msg.download()
        if msg.document:
            return await m.reply_document(dl, caption=msg.caption, reply_markup=markup)
        elif msg.video:
            return await m.reply_video(dl, caption=msg.caption, reply_markup=markup)
        elif msg.photo:
            return await m.reply_photo(dl, caption=msg.caption, reply_markup=markup)
        elif msg.animation:
            return await m.reply_animation(dl, caption=msg.caption, reply_markup=markup)
        else:
            return None
    finally:
        if os.path.exists(dl):
            os.remove(dl)
