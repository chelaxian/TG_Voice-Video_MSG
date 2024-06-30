import os
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from config import api_id, api_hash, botfather_token, language, allowed_user_id, max_file_size_mb, audio_formats, video_formats
from messages import get_message
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video, cleanup_files, split_audio_file, split_video_file
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize telethon client with bot token
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=botfather_token)

user_file_path = None
service_message_ids = []
media_message_ids = []
bot_active = False

def generate_waveform():
    # Генерация случайной waveform
    waveform = np.random.randint(0, 256, size=80, dtype=np.uint8)
    return waveform.tobytes()

async def send_welcome_message():
    welcome_message = get_message("welcome", language)
    me = await client.get_me()
    await client.send_message(me.id, welcome_message, parse_mode='markdown', silent=True)
    await client.pin_message(me.id, (await client.get_messages(me.id, limit=1))[0].id)

@client.on(events.NewMessage(pattern='/start_voice_video_bot'))
async def start(event):
    global user_file_path, bot_active
    if str(event.sender_id) not in allowed_user_id:
        return

    bot_active = True
    user_file_path = None
    msg1 = await event.reply(get_message("start", language))
    msg2 = await event.reply(get_message("send_file", language))
    service_message_ids.extend([msg1.id, msg2.id])

@client.on(events.NewMessage(pattern='/stop_voice_video_bot'))
async def stop(event):
    global user_file_path, bot_active
    if str(event.sender_id) not in allowed_user_id:
        return

    bot_active = False
    user_file_path = None
    msg = await event.reply(get_message("stop", language))
    service_message_ids.append(msg.id)
    
    for msg_id in service_message_ids:
        try:
            await client.delete_messages(event.chat_id, msg_id)
        except Exception as e:
            logging.error(f"Error deleting message {msg_id}: {e}")
    service_message_ids.clear()
    cleanup_files()

@client.on(events.NewMessage(func=lambda e: bot_active and str(e.sender_id) in allowed_user_id and e.file))
async def handle_media(event):
    global user_file_path, bot_active, service_message_ids
    if not bot_active:
        return

    file = await event.message.download_media(file=f'files/{event.message.file.name}')
    user_file_path = file

    # Проверка размера файла
    if os.path.getsize(user_file_path) > max_file_size_mb * 1024 * 1024:
        msg = await event.reply(get_message("large_file", language))
        service_message_ids.append(msg.id)
        os.remove(user_file_path)
        return

    # Проверка формата файла
    file_ext = os.path.splitext(user_file_path)[1].lower()
    if not (file_ext in audio_formats or file_ext in video_formats):
        msg = await event.reply(get_message("invalid_format", language))
        service_message_ids.append(msg.id)
        os.remove(user_file_path)
        return

    msg = await event.reply(get_message("processing_download", language))
    service_message_ids.append(msg.id)
    
    try:
        if is_audio_file(user_file_path):
            output_file, waveform, duration = convert_to_voice(user_file_path)
            await client.edit_message(event.chat_id, msg.id, get_message("processing_conversion", language))
            if os.path.getsize(output_file) > 50 * 1024 * 1024:  # Лимит на размер файла
                audio_chunks = split_audio_file(output_file)
                for chunk in audio_chunks:
                    await send_audio_chunk(event, chunk)
            else:
                waveform_data = generate_waveform()
                await client.send_file(
                    event.chat_id,
                    file=output_file,
                    voice_note=True,
                    attributes=[
                        DocumentAttributeAudio(
                            duration=duration,
                            voice=True,
                            waveform=waveform_data
                        )
                    ]
                )
            os.remove(output_file)  # Clean up the converted file
        elif is_video_file(user_file_path):
            output_file = convert_to_round_video(user_file_path)
            await client.edit_message(event.chat_id, msg.id, get_message("processing_conversion", language))
            if os.path.getsize(output_file) > 50 * 1024 * 1024:  # Лимит на размер файла
                video_chunks = split_video_file(output_file)
                for chunk in video_chunks:
                    await send_video_chunk(event, chunk)
            else:
                await client.send_file(
                    event.chat_id,
                    file=output_file,
                    video_note=True
                )
            os.remove(output_file)  # Clean up the converted file
        else:
            msg = await client.edit_message(event.chat_id, msg.id, get_message("invalid_format", language))
            service_message_ids.append(msg.id)
            user_file_path = None
            return
        await client.edit_message(event.chat_id, msg.id, get_message("processing_send", language))
    except KeyError as e:
        msg = await event.reply(f"Missing key in messages: {e}")
        service_message_ids.append(msg.id)
    except Exception as e:
        msg = await event.reply(f"Error processing file: {e}")
        service_message_ids.append(msg.id)
        user_file_path = None
        return

    msg = await event.reply(get_message("send_file", language))
    service_message_ids.append(msg.id)
    cleanup_files()

async def send_audio_chunk(event, chunk_path):
    await client.send_file(
        event.chat_id,
        file=chunk_path,
        voice_note=True
    )
    os.remove(chunk_path)  # Удаление части после отправки

async def send_video_chunk(event, chunk_path):
    await client.send_file(
        event.chat_id,
        file=chunk_path,
        video_note=True
    )
    os.remove(chunk_path)  # Удаление части после отправки

async def main():
    await client.start()
    await send_welcome_message()
    logger.info("Bot started")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
