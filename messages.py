#messages.py

from config import max_file_size_mb

def get_user_link(user_id):
    return f"tg://user?id={user_id}"

def get_group_link(group_id):
    group_id_str = str(group_id)
    if group_id_str.startswith('-100'):
        return f"https://t.me/c/{group_id_str[4:]}"
    return group_id_str

messages = {
    "welcome": {
        "RU": "Привет! Я бот для отправки голосовых сообщений и видеокружочков.\n\nКоманды:\n\n`/start_voice_video_bot` - запустить бота\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Hello! I'm a bot for sending voice messages and round videos.\n\nCommands:\n\n`/start_voice_video_bot` - start the bot\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "你好！我是用于发送语音消息和圆形视频的机器人。\n\n命令:\n\n`/start_voice_video_bot` - 启动机器人\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "start": {
        "RU": "Бот запущен.",
        "EN": "Bot started.",
        "CN": "机器人已启动。"
    },
    "stop": {
        "RU": "Бот остановлен. Файлы удалены.\n\n`/start_voice_video_bot` - запустить бота снова",
        "EN": "Bot stopped. Files deleted.\n\n`/start_voice_video_bot` - start the bot again",
        "CN": "机器人已停止。文件已删除。\n\n`/start_voice_video_bot` - 重新启动机器 人"
    },
    "send_file": {
        "RU": "Пожалуйста, отправьте аудиофайл или видеофайл.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Please send an audio or video file.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "请发送音频或视频文件。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "invalid_file": {
        "RU": f"Неверный файл. Загрузите аудиофайл или видеофайл не более {max_file_size_mb} мегабайт.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": f"Invalid file. Upload an audio or video file no larger than {max_file_size_mb} megabytes.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": f"无效的文件。上传不超过 {max_file_size_mb} 兆字节的音频或视频文件。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "large_file": {
        "RU": f"Файл слишком большой. Загрузите файл не более {max_file_size_mb} мегабайт.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": f"File is too large. Upload a file no larger than {max_file_size_mb} megabytes.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": f"文件太大。上传不超过 {max_file_size_mb} 兆字节的文件。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "invalid_format": {
        "RU": "Неверный формат файла. Пожалуйста, загрузите аудиофайл или видеофайл.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Invalid file format. Please upload an audio or video file.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "无效的文件格式。请上传音频或视频文件。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "invalid_id": {
        "RU": "Неверный формат ID. Попробуйте снова. Для групп ID должен начинаться со знака `-`.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Invalid ID format. Try again. Group IDs must start with the `-` sign.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "无效的ID格式。请再试一次。群组ID必须以 `-` 符号开头。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "send_id": {
        "RU": "Файл успешно конвертирован. Пожалуйста, отправьте ID чата/пользователя. Для групп ID должен начинаться со знака `-`.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "File successfully converted. Please send the chat/user ID. Group IDs must start with the `-` sign.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "文件转换成功。请发送聊天/用户ID。群组ID必须以 `-` 符号开头。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "send_next_id": {
        "RU": "Сообщение отправлено пользователю/группе {id}. Введите следующий ID для повторной отправки. Для групп ID должен начинаться со знака `-`.\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Message sent to user/group {id}. Enter the next ID to resend. Group IDs must start with the `-` sign.\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "消息已发送给用户/群组 {id}。输入下一个ID重新发送。群组ID必须以 `-` 符 号开头。\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "conversion_error": {
        "RU": "Ошибка при конвертации файла: {error}\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Error converting file: {error}\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "转换文件时出错：{error}\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "send_error": {
        "RU": "Ошибка при отправке сообщения: {error}\n\n`/stop_voice_video_bot` - остановить бота",
        "EN": "Error sending message: {error}\n\n`/stop_voice_video_bot` - stop the bot",
        "CN": "发送消息时出错：{error}\n\n`/stop_voice_video_bot` - 停止机器人"
    },
    "processing_conversion": {
        "RU": "Обработка файла. Пожалуйста, подождите...",
        "EN": "Processing the file. Please wait...",
        "CN": "正在处理文件。请稍候..."
    },
    "processing_download": {
        "RU": "Загрузка файла. Пожалуйста, подождите...",
        "EN": "Downloading the file. Please wait...",
        "CN": "正在下载文件。请稍候..."
    },
    "processing_send": {
        "RU": "Отправка файла. Пожалуйста, подождите...",
        "EN": "Sending the file. Please wait...",
        "CN": "正在发送文件。请稍候..."
    },
    "command_start_description": {
        "RU": "Запустить бота для обработки голосовых сообщений и видео",
        "EN": "Start the voice and video processing bot",
        "CN": "启动语音和视频处理机器人"
    },
    "command_stop_description": {
        "RU": "Остановить бота для обработки голосовых сообщений и видео",
        "EN": "Stop the voice and video processing bot",
        "CN": "停止语音和视频处理机器人"
    }
}

def get_message(key, language):
    return messages[key][language]
