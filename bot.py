import os
import logging
import asyncio
from telethon import TelegramClient, events
from config import api_id, api_hash, allowed_user_id, language, max_file_size_mb, audio_formats, video_formats
from messages import get_message, get_user_link, get_group_link
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video, cleanup_files

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('anon_session', api_id, api_hash)

user_file = None
user_chat_id = None
downloaded_file_path = None
bot_active = False
awaiting_id = False

async def send_welcome_message():
    welcome_message = get_message("welcome", language)
    me = await client.get_me()
    await client.send_message(me.id, welcome_message, parse_mode='markdown', silent=True)
    await client.pin_message(me.id, (await client.get_messages(me.id, limit=1))[0].id)

@client.on(events.NewMessage(pattern='/START_voice-video_bot'))
async def start(event):
    global bot_active, user_file, user_chat_id, awaiting_id
    if str(event.sender_id) != allowed_user_id:
        logger.warning(f"User {event.sender_id} attempted to use the bot without access.")
        return

    bot_active = True
    user_file = None
    user_chat_id = None
    awaiting_id = False
    logger.info(f"Received /START_voice-video_bot command from user {event.sender_id}")
    await event.reply(get_message("start", language))
    await event.reply(get_message("send_file", language))

@client.on(events.NewMessage(pattern='/STOP_voice-video_bot'))
async def stop(event):
    global bot_active, user_file, user_chat_id, awaiting_id
    if str(event.sender_id) != allowed_user_id:
        return

    bot_active = False
    user_file = None
    user_chat_id = None
    awaiting_id = False
    cleanup_files()
    await event.reply(get_message("stop", language))
    logger.info(f"Bot stopped by user {event.sender_id}. Files cleaned up.")

@client.on(events.NewMessage(func=lambda e: str(e.sender_id) == allowed_user_id and bot_active and e.chat_id == int(allowed_user_id) and e.file))
async def handle_media(event):
    global user_file, downloaded_file_path, awaiting_id
    logger.info(f"Received file from user {event.sender_id}")

    file = event.message.file
    if not file:
        await event.reply(get_message("invalid_file", language))
        logger.warning(f"User {event.sender_id} sent an invalid file.")
        return

    if file.size > max_file_size_mb * 1024 * 1024:
        await event.reply(get_message("large_file", language))
        logger.warning(f"User {event.sender_id} sent a file larger than {max_file_size_mb}MB.")
        return

    logger.info(f"Downloading file from user {event.sender_id}")
    downloaded_file_path = await event.message.download_media(file='downloaded_media')
    user_file = downloaded_file_path
    logger.info(f"File downloaded to {downloaded_file_path}. Starting processing.")

    try:
        if is_audio_file(downloaded_file_path):
            convert_to_voice(downloaded_file_path)
            await event.reply(get_message("send_id", language))
        elif is_video_file(downloaded_file_path):
            convert_to_round_video(downloaded_file_path)
            await event.reply(get_message("send_id", language))
        else:
            await event.reply(get_message("invalid_format", language))
            logger.warning(f"User {event.sender_id} sent a file with unsupported format.")
            user_file = None
        awaiting_id = True
    except Exception as e:
        await event.reply(get_message("conversion_error", language).format(error=e))
        logger.error(f"Error during file conversion: {e}")
        user_file = None

@client.on(events.NewMessage(func=lambda e: str(e.sender_id) == allowed_user_id and bot_active and e.chat_id == int(allowed_user_id) and not e.file))
async def handle_id(event):
    global user_chat_id, user_file, awaiting_id
    if not awaiting_id:
        return

    chat_id = event.message.text.strip()
    if not chat_id.lstrip('-').isdigit():
        awaiting_id = True
        await event.reply(get_message("invalid_id", language))
        return

    user_chat_id = int(chat_id)
    await send_media_message(event)
    awaiting_id = True  # Оставляем awaiting_id в True для ожидания следующего ID

async def send_media_message(event):
    global user_chat_id, user_file
    try:
        if is_audio_file(user_file):
            await client.send_file(user_chat_id, 'converted_voice.ogg', voice_note=True)
        elif is_video_file(user_file):
            await client.send_file(user_chat_id, 'converted_video.mp4', video_note=True)
        link = get_user_link(user_chat_id) if user_chat_id > 0 else get_group_link(user_chat_id)
        await event.reply(get_message("send_next_id", language).format(id=link), parse_mode='markdown')
    except Exception as e:
        await event.reply(get_message("send_error", language).format(error=e))

async def main():
    await client.start()
    await send_welcome_message()
    logger.info("Bot started")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

