import os
import ffmpeg
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
from scipy.io import wavfile
from config import audio_formats, video_formats

# Инициализация логгера
logger = logging.getLogger(__name__)

def is_audio_file(file_path):
    logger.info(f"Checking audio file format for: {file_path}")
    return file_path.lower().endswith(tuple(audio_formats))

def is_video_file(file_path):
    logger.info(f"Checking video file format for: {file_path}")
    return file_path.lower().endswith(tuple(video_formats))

def generate_waveform(file_path, output_path='waveform.dat'):
    try:
        wav_path = 'temp.wav'
        ffmpeg.input(file_path).output(wav_path).run(overwrite_output=True)

        samplerate, data = wavfile.read(wav_path)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        max_value = np.max(np.abs(data))
        if max_value > 0:
            data = data / max_value

        waveform = (data * 127 + 128).astype(np.uint8)
        waveform = waveform[:960]
        waveform_bytes = waveform.tobytes()

        with open(output_path, 'wb') as f:
            f.write(waveform_bytes)

        os.remove(wav_path)

        return waveform_bytes
    except Exception as e:
        logger.error(f"Error generating waveform: {e}")
        return None

def convert_to_voice(file_path):
    output_path = 'converted_voice.ogg'
    audio = AudioFileClip(file_path)

    if audio.duration > 600:
        audio = audio.subclip(0, 600)

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

    waveform = generate_waveform(output_path) if os.path.getsize(output_path) > 1 * 1024 * 1024 or audio.duration > 120 else None

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
    for file in ['converted_voice.ogg', 'converted_video.mp4', 'waveform.dat']:
        if os.path.exists(file):
            os.remove(file)
    for file in os.listdir('.'):
        if file.startswith('downloaded_media'):
            os.remove(file)

