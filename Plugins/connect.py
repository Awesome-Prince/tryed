import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from Database.sessions import get_session, del_session, update_session
from Database.privileges import get_privileges
from config import API_ID, API_HASH, USELESS_IMAGE, PHONE_NUMBER_IMAGE
from pyrogram.errors import (
  SessionPasswordNeeded,
  PhoneNumberInvalid,
  PhoneCodeInvalid,
  PasswordHashInvalid,
  FloodWait
)
from . import build, tryer
from templates import USELESS_MESSAGE

# Set up logging for debugging purposes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inline keyboard for the shortcut button
phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘶𝘵', url='tg://settings')]])

# Active user connections dictionary
active_connections = {}
watch_group = 69

def is_user_in_process(user_id):
    """Check if a user is currently in process of connecting."""
    return user_id in active_connections

async def handle_connection_error(user_id, message):
    """Handles errors during the connection process."""
    logger.error(f"Connection error for user {user_id}")
    active_connections.pop(user_id, None)
    await message.reply("**An error occurred during the process. The process has been terminated.**")

async def start_connection_process(user_id, message):
    """Start the connection process by asking for the phone number."""
    await message.reply_photo(PHONE_NUMBER_IMAGE, caption=(
        "**Enter Your Phone Number With Country Code. \n <pre>How To Find Number?</pre> \n"
        "You can Use Shortcut Button To Find Your Number ** \n"
        "<pre>Incase Shortcut Button Not Working Than You Need To Find Manually</pre>"
    ), reply_markup=phone_markup)
    
    cli = Client(str(user_id), api_id=API_ID, api_hash=API_HASH)
    active_connections[user_id] = [cli]
    await cli.connect()

@Client.on_message(filters.command('connect') & filters.private)
async def connect_user(_, message):
    """Handles the /connect command to start the user connection process."""
    user_id = message.from_user.id
    privileges = await get_privileges(user_id)

    # Check if the user has required privileges
    if not privileges[1]:
        return await tryer(message.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(_))
    
    # Check if session exists
    session = await get_session(user_id)
    if session:
        app = Client(str(user_id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        try:
            await app.start()
            await message.reply('**You Are Already Connected User**')
            await app.stop()
            return
        except Exception as e:
            logger.error(f"Error checking session for user {user_id}: {e}")
            await del_session(user_id)

    # If process already ongoing, notify user
    if is_user_in_process(user_id):
        return await message.reply("**Process Ongoing..., use /terminate to cancel.**")
    
    # Start the connection process
    await start_connection_process(user_id, message)

@Client.on_message(filters.private, group=watch_group)
async def handle_user_input(_, message):
    """Handles user input during the connection process."""
    user_id = message.from_user.id

    # Check if the user is in process
    if not is_user_in_process(user_id):
        return

    if not message.text or message.text.startswith("/"):
        return
    
    connection_data = active_connections[user_id]
    
    # Handle the phone number stage (Step 1)
    if len(connection_data) == 1:
        await handle_phone_number_stage(user_id, message, connection_data)
    
    # Handle OTP stage (Step 2)
    elif len(connection_data) == 3:
        await handle_otp_stage(user_id, message, connection_data)
    
    # Handle Two-Step Verification password stage (Step 3)
    elif len(connection_data) == 4:
        await handle_two_step_password_stage(user_id, message, connection_data)

async def handle_phone_number_stage(user_id, message, connection_data):
    """Handle the stage where the user enters their phone number."""
    try:
        phone_code_hash = await connection_data[0].send_code(message.text)
    except ConnectionError:
        await connection_data[0].connect()
        phone_code_hash = await connection_data[0].send_code(message.text)
    except PhoneNumberInvalid:
        active_connections.pop(user_id)
        return await message.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)
    except Exception as e:
        await handle_connection_error(user_id, message)
        return
    
    # Store the phone code hash and ask for OTP
    connection_data.append(phone_code_hash.phone_code_hash)
    await message.reply("**Enter OTP:**")
    active_connections[user_id] = connection_data

async def handle_otp_stage(user_id, message, connection_data):
    """Handle the stage where the user enters OTP."""
    otp = message.text.replace(" ", "") if " " in message.text else message.text
    connection_data.append(otp)
    active_connections[user_id] = connection_data
    
    try:
        await connection_data[0].sign_in(connection_data[1], connection_data[2], connection_data[3])
        session = await connection_data[0].export_session_string()
        await update_session(user_id, session)
        await connection_data[0].disconnect()
        active_connections.pop(user_id)
        await message.reply("**Successfully Connected..**")
    except PhoneCodeInvalid:
        active_connections.pop(user_id)
        await message.reply('**Invalid OTP!**')
    except SessionPasswordNeeded:
        await message.reply("**Enter Two Step Verification Password:**")
    except Exception as e:
        await handle_connection_error(user_id, message)
        return

async def handle_two_step_password_stage(user_id, message, connection_data):
    """Handle the stage where the user enters Two-Step Verification password."""
    password = message.text
    connection_data.append(password)
    
    try:
        await connection_data[0].check_password(password)
        await connection_data[0].sign_in(connection_data[1], connection_data[2], connection_data[3])
    except PhoneCodeInvalid:
        active_connections.pop(user_id)
        await message.reply('**Invalid OTP!**')
    except PasswordHashInvalid:
        active_connections.pop(user_id)
        await message.reply('**Invalid Two-Step Verification Password.**')
    except Exception as e:
        await handle_connection_error(user_id, message)
        return
    
    session = await connection_data[0].export_session_string()
    await update_session(user_id, session)
    await connection_data[0].disconnect()
    active_connections.pop(user_id)
    await message.reply("**Connected Successfully.**")

@Client.on_message(filters.command("terminate"))
async def terminate_connection(_, message):
    """Handles the /terminate command to stop an ongoing connection process."""
    user_id = message.from_user.id
    if not is_user_in_process(user_id):
        return await message.reply("**No process is ongoing to terminate.**")
    
    active_connections.pop(user_id)
    await message.reply("**Process Terminated.**")
