# Voice-Video Telegram Bot
![image](https://github.com/chelaxian/TG_Voice-Video_MSG/assets/69438111/5ceb364e-7f3a-42f8-a7ff-27eedba8bec8)

## Description
This bot allows you to send any custom voice messages and round videos to specified users or groups in Telegram. The bot supports Russian, English, and Chinese languages.
The bot trims the sent video to 1 minute to fit into Telegram's 1 minute limit for video messages.
The bot truncates sent audio up to 10 minutes to fit within Telegram's 10-minute limit for voice message transcription.

## Installation

### Prerequisites
- Python 3.10+
- telethon==1.21.1
- ffmpeg-python==0.2.0
- moviepy==1.0.3
- scipy==1.10.1
- numpy==1.24.3
- Pillow==9.3.0

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
    # config.py

    # Your API ID from my.telegram.org
    # Ваш API ID с my.telegram.org
    # 你的API ID在my.telegram.org
    api_id = 'YOUR_API_ID'

    # Your API Hash from my.telegram.org
    # Ваш API Hash с my.telegram.org
    # 你的API Hash在my.telegram.org
    api_hash = 'YOUR_API_HASH'

    # Your Telegram user ID
    # Ваш Telegram user ID
    # 你的Telegram用户ID
    allowed_user_id = 'YOUR_USER_ID'

    # Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
    # Настройка языка: 'RU' для русского, 'EN' для английского, 'CN' для китайского
    # 语言设置: 'RU' 表示俄语, 'EN' 表示英语, 'CN' 表示中文
    language = 'RU'
    #language = 'EN'
    #language = 'CN'

    # Maximum file size in megabytes
    # Максимальный размер файла в мегабайтах
    # 文件的最大大小(以兆字节为单位)
    max_file_size_mb = 100

    # Supported audio formats
    # Поддерживаемые аудио форматы
    # 支持的音频格式
    audio_formats = ['.mp3', '.wav', '.ogg', '.oga', '.m4a']

    # Supported video formats
    # Поддерживаемые видео форматы
    # 支持的视频格式
    video_formats = ['.mp4', '.mkv', '.avi', '.mov']
    ```

### Running the Bot

1. **Run the bot:**
   
    ```sh
    python3 bot.py
    ```
    Upon first run, you will be prompted to enter your phone number, the verification code sent to your Telegram, and your cloud password (if enabled).

### Usage

1. **Start the bot:**
    Send `/START_voice-video_bot` to your Telegram "Saved Messages" chat.

2. **Send a file:**
    Upload or repost an audio or video file to the "Saved Messages" chat.

3. **Provide chat/user ID:**
    After the file is processed, the bot will send you converted file and ask for the chat/user ID to send the file to. Enter the chat/user ID.
   
    To get user/group ID you can search any bot in Telegram named like "Get My ID" or similar. For example https://t.me/getmy_idbot
   
    Or you can use custom Telegram client like Swiftgram / Nicegram / iMe that have this function too.
   
    Or you can just stop the bot and repost converted file with turned on option "hide sender name".

5. **Stop the bot:**
    Send `/STOP_voice-video_bot` to your Telegram "Saved Messages" chat.

### Obtaining API ID and Hash

1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your phone number and login code.
3. Go to the API development tools section.
4. Create a new application and obtain the `api_id` and `api_hash`.

### Notes
- No BotFather token needed! Works with your Telegram account directly! 
- Ensure the API ID / Hash and your user ID are correctly set in the config.py file.
- The bot only responds to commands from the allowed user ID specified in the config.py file.
- For user IDs, use the format `xxxxxxxxxx`. For group/supergroup IDs, use the format `-xxxxxxxxxx` / `-100xxxxxxxxxx`.

## Supported Languages
- Russian (RU)
- English (EN)
- Chinese (CN)
