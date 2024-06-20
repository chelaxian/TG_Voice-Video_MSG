# Telegram Voice and Video Bot

## Overview

This bot allows users to send voice messages and round videos to specified Telegram chats. It supports audio and video file processing, converting them to appropriate formats, and sending them to designated user IDs or group IDs.

## Installation

### Requirements

- Python 3.10+
- ffmpeg
- moviepy
- telethon
- pillow

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-voice-video-bot.git
    cd telegram-voice-video-bot
    ```

2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Install ffmpeg:
    - **Ubuntu:**
      ```bash
      sudo apt update
      sudo apt install ffmpeg
      ```
    - **Windows:**
      Download and install from [FFmpeg official website](https://ffmpeg.org/download.html).

4. Configure the bot:
    - Rename `config.py.example` to `config.py`.
    - Update `config.py` with your API ID, API Hash, Telegram user ID, and preferred settings.

## Configuration

### config.py

# Your API ID from my.telegram.org
# Ваш API ID с my.telegram.org
# 您从 my.telegram.org 获取的 API ID
api_id = 'YOUR_API_ID'

# Your API Hash from my.telegram.org
# Ваш API Hash с my.telegram.org
# 您从 my.telegram.org 获取的 API Hash
api_hash = 'YOUR_API_HASH'

# Your Telegram user ID
# Ваш Telegram user ID
# 您的 Telegram 用户 ID
allowed_user_id = 'YOUR_TELEGRAM_USER_ID'

# Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
# Настройка языка: 'RU' для русского, 'EN' для английского, 'CN' для китайского
# 语言设置：'RU' 代表俄语，'EN' 代表英语，'CN' 代表中文
language = 'RU'
#language = 'EN'
#language = 'CN'

# Maximum file size in megabytes
# Максимальный размер файла в мегабайтах
# 最大文件大小（以兆字节为单位）
max_file_size_mb = 100

# Supported audio formats
# Поддерживаемые аудио форматы
# 支持的音频格式
audio_formats = ['.mp3', '.wav', '.ogg', '.oga', '.m4a']

# Supported video formats
# Поддерживаемые видео форматы
# 支持的视频格式
video_formats = ['.mp4', '.mkv', '.avi', '.mov']
Usage
Running the Bot

python bot.py
Interaction Instructions
Start the bot:
Send /START_voice-video_bot in your Telegram "Saved Messages" chat to start the bot.

Stop the bot:
Send /STOP_voice-video_bot to stop the bot.

Send a file:
Send an audio or video file in the "Saved Messages" chat. The bot will process the file and ask for the target chat/user ID.

Specify the target chat/user ID:
Enter the target chat/user ID where you want to send the processed file.

Obtaining Tokens and IDs
API ID and Hash:

Go to my.telegram.org and log in.
Navigate to "API Development Tools".
Create a new application to get your API ID and API Hash.
Telegram User ID:

Use the userinfobot in Telegram to get your user ID.
Chat/Group IDs:

For user IDs, use the format tg://user?id=USER_ID.
For group IDs, use the format -100GROUP_ID.
Troubleshooting
Ensure all dependencies are installed correctly.
Check the config.py file for correct values.
Ensure ffmpeg is installed and accessible from the command line.
License
This project is licensed under the MIT License.

概述
此机器人允许用户将语音消息和圆形视频发送到指定的Telegram聊天。它支持音频和视频文件处理，将它们转换为适当的格式，并发送到指定的用户ID或群组ID。

安装
要求
Python 3.10+
ffmpeg
moviepy
telethon
pillow
步骤
克隆存储库：


git clone https://github.com/yourusername/telegram-voice-video-bot.git
cd telegram-voice-video-bot
安装所需的Python包：


pip install -r requirements.txt
安装ffmpeg：

Ubuntu:

sudo apt update
sudo apt install ffmpeg
Windows:
从FFmpeg官方网站下载并安装。
配置机器人：

将config.py.example重命名为config.py。
更新config.py，输入您的API ID、API Hash、Telegram用户ID和首选设置。
配置
config.py

# Your API ID from my.telegram.org
# Ваш API ID с my.telegram.org
# 您从 my.telegram.org 获取的 API ID
api_id = 'YOUR_API_ID'

# Your API Hash from my.telegram.org
# Ваш API Hash с my.telegram.org
# 您从 my.telegram.org 获取的 API Hash
api_hash = 'YOUR_API_HASH'

# Your Telegram user ID
# Ваш Telegram user ID
# 您的 Telegram 用户 ID
allowed_user_id = 'YOUR_TELEGRAM_USER_ID'

# Language setting: 'RU' for Russian, 'EN' for English, 'CN' for Chinese
# Настройка языка: 'RU' для русского, 'EN' для английского, 'CN' для китайского
# 语言设置：'RU' 代表俄语，'EN' 代表英语，'CN' 代表中文
language = 'RU'
#language = 'EN'
#language = 'CN'

# Maximum file size in megabytes
# Максимальный размер файла в мегабайтах
# 最大文件大小（以兆字节为单位）
max_file_size_mb = 100

# Supported audio formats
# Поддерживаемые аудио форматы
# 支持的音频格式
audio_formats = ['.mp3', '.wav', '.ogg', '.oga', '.m4a']

# Supported video formats
# Поддерживаемые видео форматы
# 支持的视频格式
video_formats = ['.mp4', '.mkv', '.avi', '.mov']
使用
运行机器人

python bot.py
互动说明
启动机器人：
在您的Telegram“保存的消息”聊天中发送/START_voice-video_bot以启动机器人。

停止机器人：
发送/STOP_voice-video_bot以停止机器人。

发送文件：
在“保存的消息”聊天中发送音频或视频文件。机器人将处理文件并询问目标聊天/用户ID。

指定目标聊天/用户ID：
输入要发送处理后文件的目标聊天/用户ID。

获取令牌和ID
API ID和Hash：

访问my.telegram.org并登录。
导航到“API Development Tools”。
创建一个新的应用程序以获取您的API ID和API Hash。
Telegram用户ID：

使用Telegram中的userinfobot获取您的用户ID。
聊天/群组ID：

对于用户ID，使用格式tg://user?id=USER_ID。
对于群组ID，使用格式-100GROUP_ID。
故障排除
确保所有依赖项都已正确安装。
检查config.py文件中的正确值。
确保ffmpeg已安装并可以从命令行访问。
许可
此项目是根据MIT许可证授权的。



Feel free to replace placeholders like `https://github.com/yourusername/telegram-voice-video-bot.git` with the actual URLs and details of your project.
