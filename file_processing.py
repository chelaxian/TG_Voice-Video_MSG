import os
import ffmpeg
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
from config import audio_formats, video_formats, trim_audio_to_10_minutes

# Инициализация логгера
logger = logging.getLogger(__name__)

def is_audio_file(file_path):
    try:
        logger.info(f"Checking audio file format for: {file_path}")
        probe = ffmpeg.probe(file_path)
        for stream in probe['streams']:
            if stream['codec_type'] == 'audio' and 'video' not in [s['codec_type'] for s in probe['streams']]:
                return True
        return False
    except ffmpeg.Error as e:
        logger.error(f"ffmpeg error: {e}")
        return False

def is_video_file(file_path):
    try:
        logger.info(f"Checking video file format for: {file_path}")
        probe = ffmpeg.probe(file_path)
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                return True
        return False
    except ffmpeg.Error as e:
        logger.error(f"ffmpeg error: {e}")
        return False

def generate_waveform():
    try:
        # Генерация случайного waveform
        waveform = np.random.randint(0, 256, size=960, dtype=np.uint8)
        return waveform.tobytes()
    except Exception as e:
        logger.error(f"Error generating waveform: {e}")
        return None

def convert_to_voice(file_path):
    output_path = 'converted_voice.ogg'
    audio = AudioFileClip(file_path)

    temp_trimmed_path = None
    # Проверяем, нужно ли обрезать аудио
    if trim_audio_to_10_minutes and audio.duration > 600:
        audio = audio.subclip(0, 600)
        temp_trimmed_path = "temp_trimmed_audio.wav"
        audio.write_audiofile(temp_trimmed_path, codec='pcm_s16le')
        file_path = temp_trimmed_path
        audio = AudioFileClip(file_path)

    duration = int(audio.duration)

    probe = ffmpeg.probe(file_path)
    metadata = {}
    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            metadata.update(stream.get('tags', {}))

    metadata.update({
        'artist': 'Telegram',
        'title': 'Telegram Voice Message',
        'album': 'Telegram Voice Messages',
        'encoder': 'Lavf58.76.100'
    })

    input_file = ffmpeg.input(file_path)
    audio_output = ffmpeg.output(input_file, output_path,
                                 acodec='libopus',
                                 audio_bitrate='64k',
                                 format='ogg',
                                 application='voip',
                                 compression_level=10,
                                 ar='48000',
                                 ac=1)

    for key, value in metadata.items():
        audio_output = audio_output.global_args('-metadata', f'{key}={value}')

    audio_output = audio_output.global_args('-metadata', 'comment=Telegram Voice Message')

    audio_output.run(overwrite_output=True)

    # Генерация случайного waveform для длинных файлов
    waveform = generate_waveform() if os.path.getsize(output_path) > 1 * 1024 * 1024 or audio.duration > 120 else None

    if temp_trimmed_path and os.path.exists(temp_trimmed_path):
        os.remove(temp_trimmed_path)

    return output_path, waveform, duration

def convert_to_round_video(file_path):
    clip = VideoFileClip(file_path)

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
    # Удаление известных временных файлов
    for file in ['converted_voice.ogg', 'converted_video.mp4', 'waveform.dat']:
        if os.path.exists(file):
            os.remove(file)

    # Удаление всех поддерживаемых аудио и видео файлов в директории videos
    supported_formats = [ext.lower() for ext in audio_formats + video_formats]
    for root, dirs, files in os.walk('files'):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_formats):
                os.remove(os.path.join(root, file))
