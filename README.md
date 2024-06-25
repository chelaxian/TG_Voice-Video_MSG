# Voice-Video Telegram Bot
![image](https://github.com/chelaxian/TG_Voice-Video_MSG/assets/69438111/e8901e1c-3f8c-4d25-bfe4-e27fca4bc189)

## Description
This bot allows you to repost/upload any custom video and audio files and send it as telegram's voice messages and round videos to specified users or groups in Telegram. The bot supports Russian, English, and Chinese languages. Bot can works privately in your Saved Messages or like normal public bot.
The bot trims the sent video to 1 minute to fit into Telegram's 1 minute limit for video messages.
The bot also can trims sent audio up to 10 minutes (if you want so) to fit within Telegram's 10-minute limit for voice message transcription.

## Installation

### Prerequisites
- `Python 3.10+`
- `ffmpeg-python`
- `moviepy`
  
- `telethon` (if you need private bot in your Saved Messages or if you want to add waveform to big voice messages)
- `numpy` (if you want to add waveform to big voice messages)
  
- `aiogram 2.24` (if you need botfather public bot)

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

1. **Edit the config.py file to include your own API ID, API Hash (you can leave them empty if you have no plans to use telethon), and allowed user IDs. If you need BotFather bot - also include your botfather token. Replace the placeholders with your actual values.**
   
    ```python
    # Your API ID from my.telegram.org (provide if you need private bot or want big audio to have waveform)
    api_id = 'YOUR_API_ID'

    # Your API Hash from my.telegram.org (provide if you need private bot or want big audio to have waveform)
    api_hash = 'YOUR_API_HASH'

    # BotFather token (provide if you need public bot)
    botfather_token = 'YOUR_BOTFATHER_TOKEN'

    # Add random waveform to audio files (enable / disable using telethon and numpy) (not used in bot.py)
    add_random_waveform = True
    #add_random_waveform = False

    # Trim audio to 10 minutes if it's longer (enable / disable long audio trimming)
    trim_audio_to_10_minutes = True
    #trim_audio_to_10_minutes = False

    # Allow all users to interact with the bot (not used in bot.py)
    #allow_all_users = True
    allow_all_users = False
    
    # Your Telegram user ID and allowed user IDs (provide your ID and delete/ignore others if not needed)
    allowed_user_id = ['YOUR_USER_ID', 'USER_ID2', 'USER_ID3']

    # Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
    #language = 'RU'
    language = 'EN'
    #language = 'CN'

    # Maximum file size in megabytes (adjust size as you need)
    max_file_size_mb = 100

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

1. **Run the personal bot:**
   
    ```sh
    python3 bot.py
    ```
    
    or if you need public bot:
   
    ```sh
    python3 botfather.py
    ```
    
    Upon first run, for `bot.py` you will be prompted to enter your phone number, the verification code sent to your Telegram, and your cloud password (if enabled). for `botfather.py` it is not needed.

### Usage

1. **Start the bot:**
    Send `/start_voice_video_bot` to your Telegram "Saved Messages" chat or to public bot.

2. **Send a file:**
    Upload or repost an audio or video file to the "Saved Messages" chat or to public bot.

3. **Provide chat/user ID:**
    After the file is processed, the bot will send you converted file and ask for the chat/user ID to send the file to. Enter the chat/user ID.
   
    To get user/group ID you can search any bot in Telegram named like "Get My ID" or similar. For example https://t.me/getmy_idbot or https://t.me/username_to_id_bot
   
    Or you can use custom Telegram client like Swiftgram / Nicegram / iMe that have this function too.
   
    Or you can just stop the bot and repost converted file with turned on option "hide sender name".

5. **Stop the bot:**
    Send `/stop_voice_video_bot` to your Telegram "Saved Messages" chat or to public bot.


### Obtaining API ID and Hash (and BotFather token)

1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your phone number and login code.
3. Go to the API development tools section.
4. Create a new application and obtain the `api_id` and `api_hash`.
5. For BotFather bot and token use telegram bot - @BotFather
   
### Notes
- Even for BotFather bot you still need API ID and API HASH if you want to add waveform to big voice messages, because only telethon/pyrogram can inject waveform into voice messages bigger than 1 mb ( see https://github.com/chelaxian/TG_Voice-Video_MSG/issues/1 ). API ID and API HASH are requirements for telethon. if no waveform is OK for you - you can ignore this 2 parameters and don't install telethon and numpy python modules.
- Ensure the API ID / Hash (or BotFather token) and your user ID are correctly set in the config.py file.
- The bot only responds to commands from the allowed user IDs specified in the config.py file.
- For user IDs, use the format `xxxxxxxxxx`. For group/supergroup IDs, use the format `-xxxxxxxxxx` / `-100xxxxxxxxxx`.

## Supported Languages
- Russian (RU)
- English (EN)
- Chinese (CN)
