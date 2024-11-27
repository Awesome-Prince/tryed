from pyrogram import Client, filters
from config import FSUB_1, FSUB_2, JOIN_IMAGE, MUST_VISIT_LINK, TUTORIAL_LINK
from templates import JOIN_MESSAGE
from Database.settings import get_settings
from Database.users import add_user_2
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from .join_leave import get_chats

# FSUB is a list containing the two channels to monitor for join requests
FSUB = [FSUB_1, FSUB_2]

@Client.on_chat_join_request(filters.chat(FSUB_1))
async def cjr(client: Client, request):
    """Handles the chat join request for FSUB_1"""
    
    # Fetch the invite link for the backup channel
    link = (await get_chats(client))[1].invite_link

    # Create an inline keyboard markup with buttons linking to relevant channels and tutorial
    markup = IKM([
        [
            IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=link),
            IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url=MUST_VISIT_LINK)
        ],
        [
            IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)
        ]
    ])

    # Fetch settings from the database
    settings = await get_settings()

    # If auto approval is disabled, reject the join request
    if not settings['auto_approval']:
        return

    # Automatically approve the join request if auto approval is enabled
    await client.approve_chat_join_request(
        request.chat.id,
        request.from_user.id
    )

    # If the join feature is disabled in settings, do nothing further
    if not settings["join"]:
        return

    try:
        # Send the welcome message with either an image or text
        if JOIN_IMAGE:
            await client.send_photo(
                request.from_user.id, 
                JOIN_IMAGE, 
                caption=JOIN_MESSAGE.format(request.from_user.mention), 
                reply_markup=markup
            )
        else:
            await client.send_message(
                request.from_user.id, 
                JOIN_MESSAGE.format(request.from_user.mention), 
                reply_markup=markup
            )

        # Add the user to the database after successful join
        await add_user_2(request.from_user.id)

    except Exception as e:
        # Print the error message if any exception occurs
        print(f"Error in processing join request: {e}")
