import asyncio
from time import time
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from config import AUTO_DELETE_TIME
from main import app
from Database.auto_delete import get, update, get_all
from .encode_decode import decrypt, Char2Int
from templates import POST_DELETE_TEXT
from helpers import tryer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Task function
async def task():
    if AUTO_DELETE_TIME == 0:
        logging.info("Auto delete is disabled.")
        return

    logging.info("Auto delete task started.")  # Task start log

    while True:
        try:
            # Fetch all records for auto-delete
            x = await get_all()
            if not x:
                logging.info("No records found for auto-delete.")
                await asyncio.sleep(5)  # Sleep before retrying if no records exist
                continue

            for i in x:
                dic = await get(i)
                if not dic:
                    logging.warning(f"No data found for chat {i}.")
                    continue

                to_del = []  # List to keep track of the items to delete
                for z in dic:
                    then = dic[z][1]
                    if int(time() - then) >= AUTO_DELETE_TIME:
                        id_to_del = int(z)
                        id_to_edit = int(dic[z][0])
                        butt = IKM([[IKB('ᴡᴀᴛᴄʜ ᴀɢᴀɪɴ', url=dic[z][2])]])

                        # Extract count based on the link type
                        try:
                            link = dic[z][2]
                            if 'get' in link:
                                count = Char2Int(decrypt(link.split('get')[1]).split('|')[1])
                            elif 'batch' in link:
                                count = Char2Int(decrypt(link.split('batch')[1][3:]).split('|')[1])
                            else:
                                raise ValueError("Unexpected link format")
                        except Exception as e:
                            logging.error(f"Error while parsing the link for {z}: {e}")
                            continue

                        txt = POST_DELETE_TEXT.format(count)
                        to_del.append(z)

                        try:
                            # Attempt to delete and edit messages with error handling
                            await tryer(app.delete_messages, i, id_to_del)
                            await tryer(app.edit_message_text, i, id_to_edit, txt, reply_markup=butt)
                            logging.info(f"Successfully processed deletion and update for {z} in chat {i}.")
                        except Exception as e:
                            logging.error(f"Error while processing message deletion or update for {z}: {e}")

                # Remove the deleted entries from the dictionary
                for to_d in to_del:
                    del dic[to_d]

                # Update the database with the remaining data
                if dic:
                    await update(i, dic)
                else:
                    logging.warning(f"No remaining data to update for chat {i}.")

        except Exception as e:
            logging.error(f"Error in auto-delete task: {e}")

        await asyncio.sleep(1)  # Sleep before retrying the task

# Task start function
def start_task():
    asyncio.create_task(task())

# Start the task
start_task()
