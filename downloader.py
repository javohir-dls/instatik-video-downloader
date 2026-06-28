import yt_dlp
import os

def download_video(url):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        if os.path.exists(file_path):
            return file_path

    except Exception as e:
        print(e)

    return None
