from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from config import (
    FSUB_1, FSUB_2, TUTORIAL_LINK,
)
from templates import LEAVE_MESSAGE
from Database.settings import get_settings
from Plugins.start import get_chats
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

FSUB = [FSUB_1, FSUB_2]

markup = None

async def build(_):
    """Builds the inline keyboard markup with dynamic invite links for the chat."""
    global markup
    if not markup:
        chats = await get_chats(_)  # Fetch chat details
        new = []
        for chat in chats:
            # Generate invite links for the chats
            invite_link = await _.create_chat_invite_link(chat.id, creates_join_request=True)
            new.append(invite_link.invite_link)
        
        # Assign generated invite links to the chats
        for i, link in enumerate(new):
            chats[i].invite_link = link
        
        # Get the first two chats and set up the inline keyboard markup
        chat = chats[0]
        chat1 = chats[1]  # This seems unused, but could be for a future feature
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
async def jl(_: Client, cmu: ChatMemberUpdated):
    """Handles user join/leave events in the specified channels."""
    
    user = cmu.from_user
    left = cmu.old_chat_member and not cmu.new_chat_member  # Check if the user left
    joined = cmu.new_chat_member and not cmu.old_chat_member  # Check if the user joined
    
    # If the user neither joined nor left, we don't need to proceed
    if not left and not joined:
        return
    
    settings = await get_settings()
    markup = await build(_)  # Get the inline keyboard markup
    
    if joined:
        # Handle the case when the user joins
        if not settings['join']:
            return  # If joining is disabled, do nothing
        try:
            # Send a welcome message or image when the user joins
            if JOIN_IMAGE:  # Check if there is a join image
                await _.send_photo(
                    user.username if user.username else user.id,
                    JOIN_IMAGE,
                    caption=JOIN_MESSAGE.format(user.mention),  # Format the join message with user mention
                    reply_markup=markup
                )
            else:
                await _.send_message(
                    user.username if user.username else user.id,
                    JOIN_MESSAGE.format(user.mention),
                    reply_markup=markup
                )
        except Exception as e:
            print(f"Error sending join message: {e}")
    else:
        # Handle the case when the user leaves
        if not settings['leave']:
            return  # If leaving is disabled, do nothing
        try:
            # Send a leave voice message (if applicable)
            await _.send_voice(
                user.username if user.username else user.id,
                'Voice/uff.ogg',  # Path to the leave voice message
                caption=LEAVE_MESSAGE.format(user.mention),  # Format the leave message with user mention
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error sending leave message: {e}")
