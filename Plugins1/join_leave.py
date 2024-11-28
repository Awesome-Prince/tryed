from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from config import FSUB_1, FSUB_2, JOIN_IMAGE, MUST_VISIT_LINK, TUTORIAL_LINK
from templates import JOIN_MESSAGE
from Database.settings import get_settings
from Database.users import add_user_2
from .join_leave import get_chats

# List of subscription channels
FSUB = [FSUB_1, FSUB_2]

@Client.on_chat_join_request(filters.chat(FSUB_1))
async def cjr(_: Client, r):
    """
    Handle chat join requests and approve them if auto_approval is enabled.
    """
    # Get invite link for the backup channel
    link = (await get_chats(_))[1].invite_link

    # Create markup for the welcome message
    markup = IKM(
      [
        [
          IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=link),
          IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url=MUST_VISIT_LINK)
        ],
        [
          IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)
        ]
      ]
    )

    settings = await get_settings()

    # If auto_approval is disabled, return
    if not settings['auto_approval']:
        return

    # Approve the chat join request
    await _.approve_chat_join_request(
        r.chat.id,
        r.from_user.id
    )

    # If sending join messages is disabled, return
    if not settings["join"]:
        return

    # Send welcome message
    try:
        if JOIN_IMAGE:
            await _.send_photo(r.from_user.id, JOIN_IMAGE, caption=JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        else:
            await _.send_message(r.from_user.id, JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        await add_user_2(r.from_user.id)
    except Exception as e:
        print(f"Failed to send join message: {e}")
