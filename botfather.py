import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType, InputFile, BotCommand
from config import botfather_token, api_id, api_hash, language, add_random_waveform
from messages import get_message
from file_processing import is_audio_file, is_video_file, convert_to_voice, convert_to_round_video

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize aiogram bot and dispatcher
bot = Bot(token=botfather_token)
dp = Dispatcher(bot)

if add_random_waveform:
    import numpy as np
    from telethon import TelegramClient
    from telethon.tl.types import DocumentAttributeAudio

    # Initialize telethon client with bot token
    session_name = 'bot_session'
    telethon_client = TelegramClient(session_name, api_id, api_hash)

    async def start_telethon_client():
        await telethon_client.start(bot_token=botfather_token)

    asyncio.get_event_loop().run_until_complete(start_telethon_client())

user_file_path = None
service_message_ids = []

def generate_waveform():
    # Генерация случайной waveform
    waveform = np.random.randint(0, 256, size=80, dtype=np.uint8)
    return waveform.tobytes()

async def set_commands():
    commands = [
        BotCommand(command="/start_voice_video_bot", description=get_message("command_start_description", language)),
        BotCommand(command="/stop_voice_video_bot", description=get_message("command_stop_description", language))
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['start_voice_video_bot'])
async def start(message: types.Message):
    global user_file_path
    user_file_path = None
    msg1 = await message.reply(get_message("start", language))
    msg2 = await message.reply(get_message("send_file", language))
    service_message_ids.extend([msg1.message_id, msg2.message_id])

@dp.message_handler(commands=['stop_voice_video_bot'])
async def stop(message: types.Message):
    global user_file_path
    user_file_path = None
    msg = await message.reply(get_message("stop", language))
    service_message_ids.append(msg.message_id)
    
    for msg_id in service_message_ids:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except Exception as e:
            logging.error(f"Error deleting message {msg_id}: {e}")
    service_message_ids.clear()

@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.VIDEO, ContentType.AUDIO])
async def handle_media(message: types.Message):
    global user_file_path
    file = await message.document.download(destination_dir='videos') if message.document else await message.video.download(destination_dir='videos') if message.video else await message.audio.download(destination_dir='videos')
    user_file_path = file.name
    msg = await message.reply(get_message("processing_download", language))
    service_message_ids.append(msg.message_id)
    
    try:
        if is_audio_file(user_file_path):
            output_file, waveform, duration = convert_to_voice(user_file_path)
            if add_random_waveform:
                waveform_data = generate_waveform()
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
            output_file = convert_to_round_video(user_file_path)
            await bot.send_video_note(
                chat_id=message.chat.id,
                video_note=InputFile(output_file)
            )
            os.remove(output_file)  # Clean up the converted file
        else:
            msg = await message.reply(get_message("invalid_format", language))
            service_message_ids.append(msg.message_id)
            user_file_path = None
            return
    except KeyError as e:
        msg = await message.reply(f"Missing key in messages: {e}")
        service_message_ids.append(msg.message_id)
    except Exception as e:
        msg = await message.reply(f"Error processing file: {e}")
        service_message_ids.append(msg.message_id)
        user_file_path = None
        return

    msg = await message.reply(get_message("send_file", language))
    service_message_ids.append(msg.message_id)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands())
    executor.start_polling(dp, skip_updates=True)
