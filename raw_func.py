import requests
import json
from config import BOT_TOKEN

# --- Base API URL ---
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# --- Utility Function for API Requests ---
def make_request(endpoint, params=None):
    """
    Utility function to make API requests to the Telegram Bot API.
    Args:
        endpoint (str): The API endpoint to call.
        params (dict, optional): Parameters to include in the request.
    Returns:
        dict: JSON response from the API.
    """
    url = BASE_URL + endpoint
    response = requests.get(url, params=params)
    return response.json()

# --- Telegram API Methods ---
def get_chat_member(chat_id, user_id):
    """
    Get information about a member in a chat.
    Args:
        chat_id (int or str): The chat ID or username (e.g., @channelusername).
        user_id (int): The user ID to query.
    Returns:
        dict: JSON response from the Telegram API.
    """
    return make_request('getChatMember', {'chat_id': chat_id, 'user_id': user_id})

def send_message(chat_id, text, reply_markup=None):
    """
    Send a text message to a chat.
    Args:
        chat_id (int or str): The chat ID or username.
        text (str): The message text.
        reply_markup (dict, optional): Inline keyboard or reply keyboard.
    Returns:
        dict: JSON response from the Telegram API.
    """
    params = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    return make_request('sendMessage', params)

def edit_message_text(chat_id, msg_id, text, reply_markup=None):
    """
    Edit the text of an existing message.
    Args:
        chat_id (int or str): The chat ID or username.
        msg_id (int): The message ID to edit.
        text (str): The new message text.
        reply_markup (dict, optional): Inline keyboard or reply keyboard.
    Returns:
        dict: JSON response from the Telegram API.
    """
    params = {'chat_id': chat_id, 'message_id': msg_id, 'text': text}
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    return make_request('editMessageText', params)

def delete_message(chat_id, msg_id):
    """
    Delete a message in a chat.
    Args:
        chat_id (int or str): The chat ID or username.
        msg_id (int): The message ID to delete.
    """
    make_request('deleteMessage', {'chat_id': chat_id, 'message_id': msg_id})

def send_document(chat_id, file_id):
    """
    Send a document to a chat.
    Args:
        chat_id (int or str): The chat ID or username.
        file_id (str): The file ID of the document.
    Returns:
        dict: JSON response from the Telegram API.
    """
    return make_request('sendDocument', {'chat_id': chat_id, 'document': file_id})

def send_video(chat_id, file_id):
    """
    Send a video to a chat.
    Args:
        chat_id (int or str): The chat ID or username.
        file_id (str): The file ID of the video.
    Returns:
        dict: JSON response from the Telegram API.
    """
    return make_request('sendVideo', {'chat_id': chat_id, 'video': file_id})

def send_photo(chat_id, photo, caption=None, reply_markup=None):
    """
    Send a photo to a chat.
    Args:
        chat_id (int or str): The chat ID or username.
        photo (str): The URL or file ID of the photo.
        caption (str, optional): Caption for the photo.
        reply_markup (dict, optional): Inline keyboard or reply keyboard.
    Returns:
        dict: JSON response from the Telegram API.
    """
    params = {'chat_id': chat_id, 'photo': photo}
    if caption:
        params['caption'] = caption
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    return make_request('sendPhoto', params)

def edit_message_caption(chat_id, msg_id, caption, reply_markup=None):
    """
    Edit the caption of an existing message.
    Args:
        chat_id (int or str): The chat ID or username.
        msg_id (int): The message ID to edit.
        caption (str): The new caption.
        reply_markup (dict, optional): Inline keyboard or reply keyboard.
    Returns:
        dict: JSON response from the Telegram API.
    """
    params = {'chat_id': chat_id, 'message_id': msg_id, 'caption': caption}
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    return make_request('editMessageCaption', params)
