from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import FSUB_1, FSUB_2, TUTORIAL_LINK
from templates import LEAVE_MESSAGE
from Database.settings import get_settings
from Plugins.start import get_chats

# List of subscription channels
FSUB = [FSUB_1, FSUB_2]
markup = None

async def build(_):
    """
    Build the inline keyboard markup for join and tutorial links.
    """
    global markup
    if not markup:
        chats = await get_chats(_)
        new_links = []
        for chat in chats:
            invite_link = await _.create_chat_invite_link(chat.id, creates_join_request=True)
            new_links.append(invite_link.invite_link)
        for i, link in enumerate(new_links):
            chats[i].invite_link = link
        markup = IKM(
            [
                [
                    IKB("ᴊᴏɪɴ ᴀɢᴀɪɴ", url=chats[0].invite_link),
                    IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url="https://t.me/Utra_XYZ/9")
                ],
                [
                    IKB('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ', url=TUTORIAL_LINK)
                ]
            ]
        )
    return markup

@Client.on_chat_member_updated(filters.chat(FSUB_1))
async def jl(_: Client, cmu: ChatMemberUpdated):
    """
    Handle chat member updates (join/leave events) and send appropriate messages.
    """
    user = cmu.from_user
    left = cmu.old_chat_member and not cmu.new_chat_member
    joined = cmu.new_chat_member and not cmu.old_chat_member
    
    if not left and not joined:
        return
    
    settings = await get_settings()
    markup = await build(_)
    
    if joined:
        """
        if not settings['join']:
            return
        try:
            if JOIN_IMAGE:
                await _.send_photo(user.username if user.username else user.id, JOIN_IMAGE, caption=JOIN_MESSAGE, reply_markup=markup)
            else:
                await _.send_message(user.username if user.username else user.id, JOIN_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
        """
        ...
    else:
        if not settings['leave']:
            return
        try:
            # if LEAVE_IMAGE:
            #     await _.send_photo(user.username if user.username else user.id, LEAVE_IMAGE, caption=LEAVE_MESSAGE, reply_markup=markup)
            # else:
            #     await _.send_message(user.username if user.username else user.id, LEAVE_MESSAGE, reply_markup=markup)
            await _.send_voice(user.username if user.username else user.id, 'Voice/uff.ogg', caption=LEAVE_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(f"Failed to send leave message: {e}")
