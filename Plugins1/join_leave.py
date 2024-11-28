from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import FSUB_1, FSUB_2, TUTORIAL_LINK
from templates import LEAVE_MESSAGE
from Database.settings import get_settings
from Plugins.start import get_chats

# List of subscription channels
FSUB = [FSUB_1, FSUB_2]

markup = None

async def build(client: Client):
    """
    Build the markup with invite links for the subscription channels.
    """
    global markup
    if not markup:
        chats = await get_chats(client)
        new_links = []
        for chat in chats:
            invite_link = await client.create_chat_invite_link(chat.id, creates_join_request=True)
            new_links.append(invite_link.invite_link)
        for i, invite_link in enumerate(new_links):
            chats[i].invite_link = invite_link
        chat = chats[0]
        markup = IKM(
            [
                [
                    IKB("ᴊᴏɪɴ ᴀɢᴀɪɴ", url=chat.invite_link),
                    IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url="https://t.me/Utra_XYZ/9")
                ],
                [
                    IKB('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ', url=TUTORIAL_LINK)
                ]
            ]
        )
    return markup

@Client.on_chat_member_updated(filters.chat(FSUB_1))
async def jl(client: Client, chat_member_update: ChatMemberUpdated):
    """
    Handle chat member updates (join/leave events).
    """
    user = chat_member_update.from_user
    left = chat_member_update.old_chat_member and not chat_member_update.new_chat_member
    joined = chat_member_update.new_chat_member and not chat_member_update.old_chat_member
    if not left and not joined:
        return
    settings = await get_settings()
    markup = await build(client)
    if joined:
        """
        if not settings['join']:
            return
        try:
            if JOIN_IMAGE:
                await client.send_photo(user.username if user.username else user.id, JOIN_IMAGE, caption=JOIN_MESSAGE, reply_markup=markup)
            else:
                await client.send_message(user.username if user.username else user.id, JOIN_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
        """
        ...
    else:
        if not settings['leave']:
            return
        try:
            # if LEAVE_IMAGE:
            #     await client.send_photo(user.username if user.username else user.id, LEAVE_IMAGE, caption=LEAVE_MESSAGE, reply_markup=markup)
            # else:
            #     await client.send_message(user.username if user.username else user.id, LEAVE_MESSAGE, reply_markup=markup)
            await client.send_voice(user.username if user.username else user.id, 'Voice/uff.ogg', caption=LEAVE_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)