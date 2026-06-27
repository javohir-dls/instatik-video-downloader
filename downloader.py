import yt_dlp
import os

def download_video(url: str):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if not info:
            return None

        file_path = ydl.prepare_filename(info)

    file_path = os.path.splitext(file_path)[0] + ".mp4"

    if os.path.exists(file_path):
        return file_path

    return None
