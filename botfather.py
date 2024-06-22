import logging
import os
import numpy as np
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType, InputFile
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
from config import botfather_token, api_id, api_hash, language
from messages import get_message
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize aiogram bot and dispatcher
bot = Bot(token=botfather_token)
dp = Dispatcher(bot)

# Initialize telethon client with bot token
session_name = 'bot_session'
telethon_client = TelegramClient(session_name, api_id, api_hash)

async def start_telethon_client():
    await telethon_client.start(bot_token=botfather_token)

asyncio.get_event_loop().run_until_complete(start_telethon_client())

user_file_path = None

def generate_waveform():
    # Генерация случайной waveform
    waveform = np.random.randint(0, 256, size=80, dtype=np.uint8)
    return waveform.tobytes()

@dp.message_handler(commands=['start_voice_video_bot'])
async def start(message: types.Message):
    global user_file_path
    user_file_path = None
    await message.reply(get_message("start", language))
    await message.reply(get_message("send_file", language))

@dp.message_handler(commands=['stop_voice_video_bot'])
async def stop(message: types.Message):
    global user_file_path
    user_file_path = None
    await message.reply(get_message("stop", language))

@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.VIDEO, ContentType.AUDIO])
async def handle_media(message: types.Message):
    global user_file_path
    file = await message.document.download(destination_dir='videos') if message.document else await message.video.download(destination_dir='videos') if message.video else await message.audio.download(destination_dir='videos')
    user_file_path = file.name
    await message.reply(get_message("processing_download", language))
    
    try:
        if is_audio_file(user_file_path):
            await message.reply(get_message("send_file", language))
            output_file, waveform, duration = convert_to_voice(user_file_path)
            waveform_data = generate_waveform()
            if os.path.getsize(output_file) > 1 * 1024 * 1024 or duration > 120:
                async with telethon_client:
                    await telethon_client.send_file(
                        message.chat.id,
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
                await bot.send_voice(
                    chat_id=message.chat.id,
                    voice=InputFile(output_file),
                    duration=duration
                )
            os.remove(output_file)  # Clean up the converted file
        elif is_video_file(user_file_path):
            await message.reply(get_message("send_file", language))
            output_file = convert_to_round_video(user_file_path)
            async with telethon_client:
                await telethon_client.send_file(
                    message.chat.id,
                    file=output_file,
                    video_note=True
                )
            os.remove(output_file)  # Clean up the converted file
        else:
            await message.reply(get_message("invalid_format", language))
            user_file_path = None
            return
    except KeyError as e:
        await message.reply(f"Missing key in messages: {e}")
    except Exception as e:
        await message.reply(f"Error processing file: {e}")

    await message.reply(get_message("send_file", language))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
