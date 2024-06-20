import os
import ffmpeg
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
from config import audio_formats, video_formats

# Инициализация логгера
logger = logging.getLogger(__name__)

def is_audio_file(file_path):
    logger.info(f"Checking audio file format for: {file_path}")
    return file_path.lower().endswith(tuple(audio_formats))

def is_video_file(file_path):
    logger.info(f"Checking video file format for: {file_path}")
    return file_path.lower().endswith(tuple(video_formats))

def convert_to_voice(file_path):
    output_path = 'converted_voice.ogg'
    audio = AudioFileClip(file_path)

    # Обрезка аудиофайлов до 10 минут (600 секунд) для транскрибации
    if audio.duration > 600:
        audio = audio.subclip(0, 600)

    # Получение метаданных из исходного файла
    probe = ffmpeg.probe(file_path)
    metadata = {}
    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            metadata.update(stream.get('tags', {}))

    # Обновление и добавление новых метаданных
    metadata.update({
        'artist': 'Telegram',
        'title': 'Telegram Voice Message',
        'album': 'Telegram Voice Messages',
        'encoder': 'Lavf58.76.100'
    })

    # Формирование команды ffmpeg
    input_file = ffmpeg.input(file_path)
    audio_output = ffmpeg.output(input_file, output_path,
                                 acodec='libopus',
                                 audio_bitrate='64k',
                                 format='ogg',
                                 application='voip',
                                 compression_level=10,
                                 ar='48000',
                                 ac=1)

    # Добавление метаданных
    for key, value in metadata.items():
        audio_output = audio_output.global_args('-metadata', f'{key}={value}')

    # Добавление комментариев
    audio_output = audio_output.global_args(
        '-metadata', 'comment=Telegram Voice Message'
    )

    # Выполнение команды ffmpeg
    audio_output.run(overwrite_output=True)

    return output_path

def convert_to_round_video(file_path):
    clip = VideoFileClip(file_path)

    # Обрезка видео до 60 секунд
    if clip.duration > 60:
        clip = clip.subclip(0, 60)

    min_dimension = min(clip.size)
    x_center = (clip.size[0] - min_dimension) // 2
    y_center = (clip.size[1] - min_dimension) // 2
    clip = clip.crop(x1=x_center, y1=y_center, x2=x_center + min_dimension, y2=y_center + min_dimension)
    temp_file_path = "temp_square_video.mp4"
    clip.write_videofile(temp_file_path, codec='libx264', audio_codec='aac')
    output_path = 'converted_video.mp4'
    ffmpeg.input(temp_file_path).output(output_path, vf='scale=320:320,format=yuv420p', vcodec='libx264', video_bitrate='800k').run(overwrite_output=True)
    os.remove(temp_file_path)
    return output_path

def cleanup_files():
    for file in ['converted_voice.ogg', 'converted_video.mp4']:
        if os.path.exists(file):
            os.remove(file)
    for file in os.listdir('.'):
        if file.startswith('downloaded_media'):
            os.remove(file)
