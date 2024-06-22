import os
import logging
import asyncio
from telethon import TelegramClient, events
from config import api_id, api_hash, allowed_user_id, language, max_file_size_mb, audio_formats, video_formats, trim_audio_to_10_minutes
from messages import get_message, get_user_link, get_group_link
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video, cleanup_files
from telethon.tl.types import DocumentAttributeAudio

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('anon_session', api_id, api_hash)

user_file = None
user_chat_id = None
downloaded_file_path = None
bot_active = False
awaiting_id = False
processing_messages = []

async def send_welcome_message():
    welcome_message = get_message("welcome", language)
    me = await client.get_me()
    await client.send_message(me.id, welcome_message, parse_mode='markdown', silent=True)
    await client.pin_message(me.id, (await client.get_messages(me.id, limit=1))[0].id)

@client.on(events.NewMessage(pattern='/start_voice_video_bot'))
async def start(event):
    global bot_active, user_file, user_chat_id, awaiting_id, processing_messages
    if str(event.sender_id) not in allowed_user_id:
        logger.warning(f"User {event.sender_id} attempted to use the bot without access.")
        return

    bot_active = True
    user_file = None
    user_chat_id = None
    awaiting_id = False
    processing_messages = []
    logger.info(f"Received /start_voice_video_bot command from user {event.sender_id}")
    start_message = await event.reply(get_message("start", language))
    processing_messages.append(start_message.id)
    send_file_message = await event.reply(get_message("send_file", language))
    processing_messages.append(send_file_message.id)

@client.on(events.NewMessage(pattern='/stop_voice_video_bot'))
async def stop(event):
    global bot_active, user_file, user_chat_id, awaiting_id, processing_messages
    if str(event.sender_id) not in allowed_user_id:
        return

    bot_active = False
    user_file = None
    user_chat_id = None
    awaiting_id = False
    cleanup_files()
    stop_message = await event.reply(get_message("stop", language))
    logger.info(f"Bot stopped by user {event.sender_id}. Files cleaned up.")
    processing_messages.append(stop_message.id)

    for msg_id in processing_messages:
        try:
            await client.delete_messages(event.chat_id, msg_id)
        except Exception as e:
            logger.error(f"Error deleting message {msg_id}: {e}")
    processing_messages = []

@client.on(events.NewMessage(func=lambda e: str(e.sender_id) in allowed_user_id and bot_active and str(e.chat_id) in allowed_user_id and e.file))
async def handle_media(event):
    global user_file, downloaded_file_path, awaiting_id, processing_messages
    logger.info(f"Received file from user {event.sender_id}")

    file = event.message.file
    if not file:
        invalid_file_message = await event.reply(get_message("invalid_file", language))
        processing_messages.append(invalid_file_message.id)
        logger.warning(f"User {event.sender_id} sent an invalid file.")
        return

    if file.size > max_file_size_mb * 1024 * 1024:
        large_file_message = await event.reply(get_message("large_file", language))
        processing_messages.append(large_file_message.id)
        logger.warning(f"User {event.sender_id} sent a file larger than {max_file_size_mb}MB.")
        return

    logger.info(f"Downloading file from user {event.sender_id}")

    download_message = await event.reply(get_message("processing_download", language))
    processing_messages.append(download_message.id)

    file_ext = os.path.splitext(file.name)[1] if file.name else '.ogg'
    downloaded_file_path = await event.message.download_media(file=f'downloaded_media{file_ext}')
    user_file = downloaded_file_path
    logger.info(f"File downloaded to {downloaded_file_path}. Starting processing.")

    await client.delete_messages(event.chat_id, download_message.id)

    logger.info(f"Downloaded file path: {downloaded_file_path}")

    processing_message = await event.reply(get_message("processing_conversion", language))
    processing_messages.append(processing_message.id)

    try:
        logger.info(f"Checking if file is audio: {downloaded_file_path}")
        if is_audio_file(downloaded_file_path):
            logger.info("File is an audio file, converting to voice message.")
            output_file, waveform, duration = convert_to_voice(downloaded_file_path)
            await client.send_file(event.chat_id, output_file, voice_note=True, attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    voice=True,
                    waveform=waveform
                )
            ])
            send_id_message = await event.reply(get_message("send_id", language))
            processing_messages.append(send_id_message.id)
        elif is_video_file(downloaded_file_path):
            logger.info("File is a video file, converting to round video.")
            output_file = convert_to_round_video(downloaded_file_path)
            await client.send_file(event.chat_id, output_file, video_note=True)
            send_id_message = await event.reply(get_message("send_id", language))
            processing_messages.append(send_id_message.id)
        else:
            invalid_format_message = await event.reply(get_message("invalid_format", language))
            processing_messages.append(invalid_format_message.id)
            logger.warning(f"User {event.sender_id} sent a file with unsupported format.")
            user_file = None
        awaiting_id = True
    except Exception as e:
        conversion_error_message = await event.reply(get_message("conversion_error", language).format(error=e))
        processing_messages.append(conversion_error_message.id)
        logger.error(f"Error during file conversion: {e}")
        user_file = None

    await client.delete_messages(event.chat_id, processing_message.id)

@client.on(events.NewMessage(func=lambda e: str(e.sender_id) in allowed_user_id and bot_active and str(e.chat_id) in allowed_user_id and not e.file))
async def handle_id(event):
    global user_chat_id, user_file, awaiting_id, processing_messages
    if not awaiting_id:
        return

    chat_id = event.message.text.strip()
    if not chat_id.lstrip('-').isdigit():
        invalid_id_message = await event.reply(get_message("invalid_id", language))
        processing_messages.append(invalid_id_message.id)
        awaiting_id = True
        return

    user_chat_id = int(chat_id)
    await send_media_message(event)
    awaiting_id = True

async def send_media_message(event):
    global user_chat_id, user_file, processing_messages
    try:
        sending_message = await event.reply(get_message("processing_send", language))
        processing_messages.append(sending_message.id)

        if is_audio_file(user_file):
            output_file, waveform, duration = convert_to_voice(user_file)
            await client.send_file(user_chat_id, output_file, voice_note=True, attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    voice=True,
                    waveform=waveform
                )
            ])
        elif is_video_file(user_file):
            output_file = convert_to_round_video(user_file)
            await client.send_file(user_chat_id, output_file, video_note=True)

        link = get_user_link(user_chat_id) if user_chat_id > 0 else get_group_link(user_chat_id)
        send_next_id_message = await event.reply(get_message("send_next_id", language).format(id=link), parse_mode='markdown')
        processing_messages.append(send_next_id_message.id)

        await client.delete_messages(event.chat_id, sending_message.id)
    except Exception as e:
        send_error_message = await event.reply(get_message("send_error", language).format(error=e))
        processing_messages.append(send_error_message.id)

async def main():
    await client.start()
    await send_welcome_message()
    logger.info("Bot started")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
