# Voice-Video Telegram Bot
![image](https://github.com/chelaxian/TG_Voice-Video_MSG/assets/69438111/e8901e1c-3f8c-4d25-bfe4-e27fca4bc189)

## Description
This bot allows you to repost/upload any custom video and audio files and send it as telegram's voice messages and round videos to specified users or groups in Telegram. The bot supports Russian, English, and Chinese languages. 
## Installation

### Prerequisites
- `Python 3.10+`
- `ffmpeg-python`
- `moviepy`
  
- `telethon` 
- `numpy`
  
- `aiogram 2.24`

### Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/chelaxian/TG_Voice-Video_MSG.git
    cd TG_Voice-Video_MSG
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install ffmpeg:**
    - For Ubuntu:
        ```sh
        sudo apt update
        sudo apt install ffmpeg
        ```
    - For Windows:
        Download the installer from [ffmpeg.org](https://ffmpeg.org/download.html) and follow the installation instructions.

### Configuration

1. **Edit the config.py file to include your own API ID, API Hash, and allowed user IDs. Also include your botfather token. Replace the placeholders with your actual values.**
   
    ```python
    # Your API ID from my.telegram.org
    api_id = 'YOUR_API_ID'

    # Your API Hash from my.telegram.org 
    api_hash = 'YOUR_API_HASH'

    # BotFather token
    botfather_token = 'YOUR_BOTFATHER_TOKEN'

    # Allow all users to interact with the bot 
    #allow_all_users = True
    allow_all_users = False
    
    # Your Telegram user ID and allowed user IDs 
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
    ```

### Running the Bot

1. **Run the bot:**
   
    ```sh
    python3 bot.py
    ```

### Usage

1. **Start the bot:**
    Send `/start_voice_video_bot` to your Telegram bot.

2. **Send a file:**
    Upload or repost an audio or video file to the bot.

3. **Provide chat/user ID:**
    After the file is processed, the bot will send you converted file.
    To send voice/video from your sender name you can stop the bot and repost converted file with turned on telegram option "hide sender name".

5. **Stop the bot:**
    Send `/stop_voice_video_bot` to your Telegram bot.


### Obtaining API ID and Hash (and BotFather token)

1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your phone number and login code.
3. Go to the API development tools section.
4. Create a new application and obtain the `api_id` and `api_hash`.
5. For BotFather bot and token use telegram bot - @BotFather
   
### Notes
- You need API ID and API HASH because only telethon/pyrogram can inject waveform into voice messages bigger than 1 mb ( see https://github.com/chelaxian/TG_Voice-Video_MSG/issues/1 ). API ID and API HASH are requirements for telethon.
- Ensure the API ID / Hash and BotFather token and your user ID are correctly set in the config.py file.
- The bot only responds to commands from the allowed user IDs specified in the config.py file.

## Supported Languages
- Russian (RU)
- English (EN)
- Chinese (CN)
