from os import getenv

# Configuration from environment variables
API_ID = int(getenv('API_ID', '28982634'))
API_HASH = getenv('API_HASH', 'b54ae7b2e6a8874f82c860ec22e2a3df')
BOT_TOKEN = getenv('BOT_TOKEN', '8119715618:AAH-rYQ84LA-PdvCF90A1qSfILUQuzKTBo0')
BOT_TOKEN_2 = getenv('BOT_TOKEN_2', '7208277760:AAGKBNndrcUIjl596wgcpi9SKfiiCOROy8Q')

SUDO_USERS = getenv('SUDO_USERS', '6604279354 6104594076')  # Example: '1234 6789'
MONGO_DB_URI = getenv('MONGO_DB_URI', 'mongodb+srv://Manik:manik11@cluster0.xtzuh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

DB_CHANNEL_ID = int(getenv('DB_CHANNEL_ID', '-1002230637444'))
DB_CHANNEL_2_ID = int(getenv('DB_CHANNEL_2_ID', '-1002296508906'))
LOG_CHANNEL_ID = getenv('LOG_CHANNEL_ID', '-1002462410192')  # Keep it Empty if no Log Channel  

AUTO_DELETE_TIME = int(getenv('AUTO_DELETE_TIME', '3600'))  # Enter time in seconds, keep it 0 for disabling.

FSUB_1 = -1002210532935
FSUB_2 = -1002319501979

MUST_VISIT_LINK = "https://t.me/Ultra_XYZ/14"
LINK_GENERATE_IMAGE = getenv('LINK_GENERATE_IMAGE', 'https://graph.org/file/a1cce5b8533180c2f0029.jpg')
TUTORIAL_LINK = getenv('TUTORIAL_LINK', 'https://t.me/Ultra_XYZ/16')
CONNECT_TUTORIAL_LINK = getenv('CONNECT_TUTORIAL_LINK', 'https://t.me/Terabox_Sharing_Bot?start=batchoneaWZkYS1pZmRjfGhoZg==')
SU_IMAGE = "https://graph.org/file/2342d37844afd1b9b96c0.jpg"

# JOIN
JOIN_MESSAGE = getenv('JOIN_MESSAGE', 'You Joined.')
JOIN_IMAGE = getenv('JOIN_IMAGE', 'https://graph.org/file/015fddf0dbeb03b639647.jpg')

# LEAVE
LEAVE_CAPTION = getenv('LEAVE_CAPTION', 'I Love You.')

# USELESS IMAGE AND MESSAGE
USELESS_MESSAGE = getenv('USELESS_MESSAGE', 'This is useless text.')
USELESS_IMAGE = getenv('USELESS_IMAGE', 'https://graph.org/file/c579032c65d8353e43b0f.jpg')

STICKER_ID = 'CAACAgUAAxkBAAIiHWZjPezFGPWT_87VHnJUaschvGtrAAJtDgACYpoYV06rLlLA8dv_HgQ'
CONTENT_SAVER = True
EXPIRY_TIME = 30  # In days
AUTO_SAVE_CHANNEL_ID = -1002362025379
PHONE_NUMBER_IMAGE = "https://graph.org/file/2821554b6b082eb8741dc.jpg"
WARN_IMAGE = 'https://graph.org/file/c86c68e014e471c1ce729.jpg'

# DO NOT CHANGE BELOW CODES.
SUDO_USERS = [int(x) for x in SUDO_USERS.split()]
LOG_CHANNEL_ID = int(LOG_CHANNEL_ID) if LOG_CHANNEL_ID else None
