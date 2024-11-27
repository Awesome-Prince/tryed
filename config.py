from os import getenv

# --- Basic Configuration ---
API_ID = int(getenv('API_ID', '28982634'))
API_HASH = getenv('API_HASH', 'b54ae7b2e6a8874f82c860ec22e2a3df')
BOT_TOKEN = getenv('BOT_TOKEN', '7773860912:AAHo6aHZcV61VvaF_ymqY6_n7bneICOBbfo')
BOT_TOKEN_2 = getenv('BOT_TOKEN_2', '8119715618:AAH-rYQ84LA-PdvCF90A1qSfILUQuzKTBo0')

# --- User and Database Configuration ---
SUDO_USERS = [int(x) for x in getenv('SUDO_USERS', '6604279354 6104594076').split()]  # Example: '1234 6789'
MONGO_DB_URI = getenv(
    'MONGO_DB_URI', 
    'mongodb+srv://Manik:manik11@cluster0.xtzuh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
)
DB_CHANNEL_ID = int(getenv('DB_CHANNEL_ID', '-1002230637444'))
DB_CHANNEL_2_ID = int(getenv('DB_CHANNEL_2_ID', '-1002296508906'))

# --- Logging Configuration ---
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', '0')) or None  # None if no Log Channel

# --- Timer Configuration ---
AUTO_DELETE_TIME = int(getenv('AUTO_DELETE_TIME', '3600'))  # Time in seconds (0 disables auto-delete)

# --- String to display auto delete time ---
AUTO_DELETE_STR = f"Auto delete will happen in {AUTO_DELETE_TIME} seconds."

# --- Subscription Channels ---
FSUB_1 = int(getenv('FSUB_1', '-1002210532935'))
FSUB_2 = int(getenv('FSUB_2', '-1002319501979'))

# --- Links and Images ---
MUST_VISIT_LINK = getenv('MUST_VISIT_LINK', 'https://t.me/Ultra_XYZ/14')
LINK_GENERATE_IMAGE = getenv('LINK_GENERATE_IMAGE', 'https://graph.org/file/a1cce5b8533180c2f0029.jpg')
TUTORIAL_LINK = getenv('TUTORIAL_LINK', 'https://t.me/Ultra_XYZ/16')
CONNECT_TUTORIAL_LINK = getenv(
    'CONNECT_TUTORIAL_LINK', 
    'https://t.me/Terabox_Sharing_Bot?start=batchoneaWZkYS1pZmRjfGhoZg=='
)
SU_IMAGE = "https://graph.org/file/2342d37844afd1b9b96c0.jpg"

# --- Join/Leave Messages ---
JOIN_MESSAGE = getenv('JOIN_MESSAGE', 'You Joined.')
JOIN_IMAGE = getenv('JOIN_IMAGE', 'https://graph.org/file/015fddf0dbeb03b639647.jpg')
LEAVE_CAPTION = getenv('LEAVE_CAPTION', 'I Love You.')

# --- Miscellaneous ---
USELESS_MESSAGE = getenv('USELESS_MESSAGE', 'This is useless text.')
USELESS_IMAGE = getenv('USELESS_IMAGE', 'https://graph.org/file/c579032c65d8353e43b0f.jpg')
STICKER_ID = 'CAACAgUAAxkBAAIiHWZjPezFGPWT_87VHnJUaschvGtrAAJtDgACYpoYV06rLlLA8dv_HgQ'
CONTENT_SAVER = True
EXPIRY_TIME = int(getenv('EXPIRY_TIME', '30'))  # Expiry time in days
AUTO_SAVE_CHANNEL_ID = int(getenv('AUTO_SAVE_CHANNEL_ID', '-1002362025379'))
PHONE_NUMBER_IMAGE = getenv('PHONE_NUMBER_IMAGE', 'https://graph.org/file/2821554b6b082eb8741dc.jpg')
WARN_IMAGE = getenv('WARN_IMAGE', 'https://graph.org/file/c86c68e014e471c1ce729.jpg')
