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
async def cjr(client: Client, join_request: ChatJoinRequest):
    """
    Approve chat join request and send a welcome message.
    """
    link = (await get_chats(client))[1].invite_link
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
    if not settings['auto_approval']:
        return
    await client.approve_chat_join_request(
        join_request.chat.id,
        join_request.from_user.id
    )
    if not settings["join"]:
        return
    try:
        if JOIN_IMAGE:
            await client.send_photo(join_request.from_user.id, JOIN_IMAGE, caption=JOIN_MESSAGE.format(join_request.from_user.mention), reply_markup=markup)
        else:
            await client.send_message(join_request.from_user.id, JOIN_MESSAGE.format(join_request.from_user.mention), reply_markup=markup)
        await add_user_2(join_request.from_user.id)
    except Exception as e:
        print(e)