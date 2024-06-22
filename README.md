# Voice-Video Telegram Bot
![image](https://github.com/chelaxian/TG_Voice-Video_MSG/assets/69438111/5ceb364e-7f3a-42f8-a7ff-27eedba8bec8)

## Description
This bot allows you to repost/upload any custom video and audio files and send it as telegram's voice messages and round videos to specified users or groups in Telegram. The bot supports Russian, English, and Chinese languages. Bot can works privately in your Saved Messages or like normal public bot.
The bot trims the sent video to 1 minute to fit into Telegram's 1 minute limit for video messages.
The bot also can trims sent audio up to 10 minutes (if you want so) to fit within Telegram's 10-minute limit for voice message transcription.

## Installation

### Prerequisites
- Python 3.10+
- telethon
- ffmpeg-python
- moviepy
- numpy
- aiogram 2.24 (if you need botfather bot too)

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

1. **Edit the config.py file to include your own API ID, API Hash, and allowed user ID. Replace the placeholders with your actual values.**
   
    ```python
    # Your API ID from my.telegram.org
    api_id = 'YOUR_API_ID'

    # Your API Hash from my.telegram.org
    api_hash = 'YOUR_API_HASH'

    # BotFather token (fill in if you need public bot too)
    botfather_token = 'YOUR_BOTFATHER_TOKEN'
    
    # Your Telegram user ID and allowed user IDs (delete others if no need)
    allowed_user_id = ['YOUR_USER_ID', 'USER_ID2', 'USER_ID3']

    # Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
    #language = 'RU'
    language = 'EN'
    #language = 'CN'

    # Maximum file size in megabytes
    max_file_size_mb = 100

    # Supported audio formats
    audio_formats = [
    '.mp3', '.wav', '.ogg', '.oga', '.m4a', '.aac', '.flac', '.alac',
    '.wma', '.aiff', '.opus', '.amr', '.mka'
    ]

    # Supported video formats
    video_formats = [
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v',
    '.mpg', '.mpeg', '.3gp', '.3g2', '.mxf', '.ogv', '.mts', '.m2ts'
    ]

    # Trim audio to 10 minutes if it's longer
    trim_audio_to_10_minutes = True
    #trim_audio_to_10_minutes = False
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
    
    Upon first run, for `bot.py` you will be prompted to enter your phone number, the verification code sent to your Telegram, and your cloud password (if enabled). for `botfather.py` it is no needed.

### Usage

1. **Start the bot:**
    Send `/start_voice_video_bot` to your Telegram "Saved Messages" chat.

2. **Send a file:**
    Upload or repost an audio or video file to the "Saved Messages" chat.

3. **Provide chat/user ID:**
    After the file is processed, the bot will send you converted file and ask for the chat/user ID to send the file to. Enter the chat/user ID.
   
    To get user/group ID you can search any bot in Telegram named like "Get My ID" or similar. For example https://t.me/getmy_idbot or https://t.me/username_to_id_bot
   
    Or you can use custom Telegram client like Swiftgram / Nicegram / iMe that have this function too.
   
    Or you can just stop the bot and repost converted file with turned on option "hide sender name".

5. **Stop the bot:**
    Send `/stop_voice_video_bot` to your Telegram "Saved Messages" chat.


### Obtaining API ID and Hash (and BotFather token)

1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your phone number and login code.
3. Go to the API development tools section.
4. Create a new application and obtain the `api_id` and `api_hash`.
5. For BotFather bot and token use telegram bot - @BotFather
### Notes
- Even for BotFather bot you still need API ID and API HASH because only telethon can inject waveform into voice messages bigger than 1 mb. API ID and API HASH are requirements for telethon. ( see https://github.com/chelaxian/TG_Voice-Video_MSG/issues/1 )
- Ensure the API ID / Hash and your user ID are correctly set in the config.py file.
- The bot only responds to commands from the allowed user IDs specified in the config.py file.
- For user IDs, use the format `xxxxxxxxxx`. For group/supergroup IDs, use the format `-xxxxxxxxxx` / `-100xxxxxxxxxx`.

## Supported Languages
- Russian (RU)
- English (EN)
- Chinese (CN)
