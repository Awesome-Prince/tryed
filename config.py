import os

class Config:
    # Bot tokens
    API_ID = int(os.getenv('API_ID', '28982634'))
    API_HASH = os.getenv('API_HASH', 'b54ae7b2e6a8874f82c860ec22e2a3df')
    BOT_TOKEN1 = os.getenv('BOT_TOKEN1', '6944717193:AAG4nhx08Ri61XnLIHhGS1dG1Ik5mlLeh5g')
    BOT_TOKEN2 = os.getenv('BOT_TOKEN2', '7208277760:AAGKBNndrcUIjl596wgcpi9SKfiiCOROy8Q')

    # Users and Database
    SUDO_USERS = [int(x) for x in os.getenv('SUDO_USERS', '6604279354 6104594076').split()]
    MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'mongodb+srv://Manik:manik11@cluster0.xtzuh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    
    # Channels and Logging
    DB_CHANNEL_ID = int(os.getenv('DB_CHANNEL_ID', '-1002230637444'))
    DB_CHANNEL2_ID = int(os.getenv('DB_CHANNEL2_ID', '-1002296508906'))
    LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', '-1002462410192')) if os.getenv('LOG_CHANNEL_ID') else None

    # Auto delete settings
    AUTO_DELETE_TIME = int(os.getenv('AUTO_DELETE_TIME', '3600'))  # Time in seconds, 0 to disable.

    # Subscription and links
    FSUB1 = int(os.getenv('FSUB1', '-1002210532935'))
    FSUB2 = int(os.getenv('FSUB2', '-1002319501979'))
    MUST_VISIT_LINK = os.getenv('MUST_VISIT_LINK', "https://t.me/Ultra_XYZ/14")
    LINK_GENERATE_IMAGE = os.getenv('LINK_GENERATE_IMAGE', 'https://graph.org/file/a1cce5b8533180c2f0029.jpg')
    TUTORIAL_LINK = os.getenv('TUTORIAL_LINK', 'https://t.me/Ultra_XYZ/16')
    CONNECT_TUTORIAL_LINK = os.getenv('CONNECT_TUTORIAL_LINK', 'https://t.me/Terabox_Sharing_Bot?start=batchoneaWZkYS1pZmRjfGhoZg==')

    # Images and messages
    SU_IMAGE = os.getenv('SU_IMAGE', 'https://graph.org/file/2342d37844afd1b9b96c0.jpg')
    JOIN_MESSAGE = os.getenv('JOIN_MESSAGE', 'You Joined.')
    JOIN_IMAGE = os.getenv('JOIN_IMAGE', 'https://graph.org/file/015fddf0dbeb03b639647.jpg')
    LEAVE_CAPTION = os.getenv('LEAVE_CAPTION', 'I Love You.')
    USELESS_MESSAGE = os.getenv('USELESS_MESSAGE', 'This is useless text.')
    USELESS_IMAGE = os.getenv('USELESS_IMAGE', 'https://graph.org/file/c579032c65d8353e43b0f.jpg')

    # Stickers and content settings
    STICKER_ID = os.getenv('STICKER_ID', 'CAACAgUAAxkBAAIiHWZjPezFGPWT_87VHnJUaschvGtrAAJtDgACYpoYV06rLlLA8dv_HgQ')
    CONTENT_SAVER = bool(os.getenv('CONTENT_SAVER', True))
    EXPIRY_TIME = int(os.getenv('EXPIRY_TIME', 30))  # In days
    AUTO_SAVE_CHANNEL_ID = int(os.getenv('AUTO_SAVE_CHANNEL_ID', '-1002362025379'))

    # Warning images
    PHONE_NUMBER_IMAGE = os.getenv('PHONE_NUMBER_IMAGE', "https://graph.org/file/2821554b6b082eb8741dc.jpg")
    WARN_IMAGE = os.getenv('WARN_IMAGE', 'https://graph.org/file/c86c68e014e471c1ce729.jpg')