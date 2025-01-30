#config.py

# Your API ID from my.telegram.org 
api_id = 'YOUR_API_ID'

# Your API Hash from my.telegram.org
api_hash = 'YOUR_API_HASH'

# BotFather token
botfather_token = 'YOUR_BOTFATHER_TOKEN'

# Allow all users to interact with the bot 
#allow_all_users = True
allow_all_users = False

# Your Telegram user ID and allowed user IDs (provide your ID and delete/ignore others if not needed)
allowed_user_id = ['YOUR_USER_ID', 'USER_ID2', 'USER_ID3']

# Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
#language = 'RU'
language = 'EN'
#language = 'CN'

# Maximum file size in megabytes (adjust size as you need)
max_file_size_mb = 50

# Supported audio formats (you can limit formats if you want to)
audio_formats = [
'.mp3', '.wav', '.ogg', '.oga', '.m4a', '.aac', '.flac', '.alac',
'.wma', '.aiff', '.opus', '.amr', '.mka'
]

# Supported video formats (you can limit formats if you want to)
video_formats = [
'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v',
'.mpg', '.mpeg', '.3gp', '.3g2', '.mxf', '.ogv', '.mts', '.m2ts'
]
