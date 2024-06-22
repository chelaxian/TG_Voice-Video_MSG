import os
import logging
import asyncio
from telethon import TelegramClient, events
from config import botfather_token, language, max_file_size_mb, audio_formats, video_formats, trim_audio_to_10_minutes
from messages import get_message, get_user_link, get_group_link
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video, cleanup_files
from telethon.tl.types import DocumentAttributeAudio

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('bot_sess', botfather_token)

@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.sender_id != client.get_me().user_id:
        return
    
    if not event.file:
        await event.reply("Please send an audio or video file to convert.")
        return

    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    file_path = await event.message.download_media('downloads/')
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    if file_size_mb > max_file_size_mb:
        await event.reply(f"File size exceeds {max_file_size_mb} MB limit.")
        os.remove(file_path)
        return
    
    if is_audio_file(file_path):
        converted_path = convert_to_voice(file_path, trim_audio_to_10_minutes)
        await event.reply(file=converted_path)
        os.remove(converted_path)
    elif is_video_file(file_path):
        converted_path = convert_to_round_video(file_path)
        await event.reply(file=converted_path)
        os.remove(converted_path)
    else:
        await event.reply("Unsupported file format.")
    
    os.remove(file_path)
    cleanup_files()

def main():
    client.start(bot_token=botfather_token)
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
