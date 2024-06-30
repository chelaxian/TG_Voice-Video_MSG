import os
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio
from config import api_id, api_hash, botfather_token, language, allowed_user_id, max_file_size_mb, audio_formats, video_formats
from messages import get_message
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video, cleanup_files

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=botfather_token)

user_file_path = None
service_message_ids = []
media_message_ids = []
bot_active = False

def generate_waveform():
    # Генерация случайной waveform
    import numpy as np
    waveform = np.random.randint(0, 256, size=80, dtype=np.uint8)
    return waveform.tobytes()

@client.on(events.NewMessage(pattern='/start_voice_video_bot'))
async def start(event):
    global bot_active
    if str(event.sender_id) not in allowed_user_id:
        return

    bot_active = True
    msg1 = await event.reply(get_message("start", language))
    msg2 = await event.reply(get_message("send_file", language))
    service_message_ids.extend([msg1.id, msg2.id])

@client.on(events.NewMessage(pattern='/stop_voice_video_bot'))
async def stop(event):
    global bot_active
    if str(event.sender_id) not in allowed_user_id:
        return

    bot_active = False
    cleanup_files()
    msg = await event.reply(get_message("stop", language))
    service_message_ids.append(msg.id)
    
    for msg_id in service_message_ids:
        try:
            await client.delete_messages(event.chat_id, msg_id)
        except Exception as e:
            logging.error(f"Error deleting message {msg_id}: {e}")
    service_message_ids.clear()

@client.on(events.NewMessage(func=lambda e: e.file and str(e.sender_id) in allowed_user_id and bot_active))
async def handle_media(event):
    global user_file_path
    file = event.message.file

    # Check file size
    if file.size > max_file_size_mb * 1024 * 1024:
        msg = await event.reply(get_message("large_file", language))
        service_message_ids.append(msg.id)
        return

    file_ext = os.path.splitext(file.name)[1].lower()
    if not (file_ext in audio_formats or file_ext in video_formats):
        msg = await event.reply(get_message("invalid_format", language))
        service_message_ids.append(msg.id)
        return

    msg = await event.reply(get_message("processing_download", language))
    service_message_ids.append(msg.id)

    downloaded_file_path = await event.message.download_media(file=f'downloaded_media{file_ext}')
    user_file_path = downloaded_file_path

    try:
        if is_audio_file(downloaded_file_path):
            output_file, waveform, duration = convert_to_voice(downloaded_file_path)
            await client.edit_message(event.chat_id, msg.id, get_message("processing_conversion", language))
            if os.path.getsize(output_file) > max_file_size_mb * 1024 * 1024 or duration > 120:
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
            else:
                await client.send_file(event.chat_id, output_file, voice_note=True)
            os.remove(output_file)
        elif is_video_file(downloaded_file_path):
            output_file = convert_to_round_video(downloaded_file_path)
            await client.edit_message(event.chat_id, msg.id, get_message("processing_conversion", language))
            await client.send_file(event.chat_id, output_file, video_note=True)
            os.remove(output_file)
        else:
            msg = await client.edit_message(event.chat_id, msg.id, get_message("invalid_format", language))
            service_message_ids.append(msg.id)
            return
        await client.edit_message(event.chat_id, msg.id, get_message("processing_send", language))
    except Exception as e:
        msg = await event.reply(f"Error processing file: {e}")
        service_message_ids.append(msg.id)

    msg = await event.reply(get_message("send_file", language))
    service_message_ids.append(msg.id)
    cleanup_files()

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
