from config import BOT_TOKEN
import requests
import json

base = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def getChatMember(chat_id, user_id):
    url = f'{base}getChatMember?chat_id={chat_id}&user_id={user_id}'
    return requests.get(url).json()

def sendMessage(chat_id, text, reply_markup=None):
    url = f'{base}sendMessage?chat_id={chat_id}&text={text}'
    if reply_markup:
        url += f'&reply_markup={json.dumps(reply_markup)}'
    return requests.get(url).json()

def editMessageText(chat_id, msg_id, text, reply_markup=None):
    url = f'{base}editMessageText?chat_id={chat_id}&message_id={msg_id}&text={text}'
    if reply_markup:
        url += f'&reply_markup={json.dumps(reply_markup)}'
    return requests.get(url).json()

def deleteMessage(chat_id, msg_id):
    url = f'{base}deleteMessage?chat_id={chat_id}&message_id={msg_id}'
    requests.get(url)

def sendDocument(chat_id, file_id):
    url = f'{base}sendDocument?chat_id={chat_id}&document={file_id}'
    return requests.get(url).json()

def sendVideo(chat_id, file_id):
    url = f'{base}sendVideo?chat_id={chat_id}&video={file_id}'
    return requests.get(url).json()

def sendPhoto(chat_id, photo, caption=None, reply_markup=None):
    url = f'{base}sendPhoto?chat_id={chat_id}&photo={photo}'
    if caption:
        url += f'&caption={caption}'
    if reply_markup:
        url += f'&reply_markup={json.dumps(reply_markup)}'
    return requests.get(url).json()

def editMessageCaption(chat_id, msg_id, caption, reply_markup=None):
    url = f'{base}editMessageCaption?chat_id={chat_id}&message_id={msg_id}&caption={caption}'
    if reply_markup:
        url += f'&reply_markup={json.dumps(reply_markup)}'
    return requests.get(url).json()
