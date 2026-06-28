import os
import uuid
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_video(url: str):
    file_id = str(uuid.uuid4())[:8]
    output = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    ydl_opts = {
        "outtmpl": output,
        "format": "worst[ext=mp4]/best[ext=mp4]/best",
        "noplaylist": True,

        # 🔥 MUHIM FIXLAR
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 15,
        "retries": 1,
        "fragment_retries": 1,
        "concurrent_fragment_downloads": 1,

        # 🔥 YouTube freeze oldini olish
        "extractor_args": {
            "youtube": {
                "skip": ["dash", "hls"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

        # always mp4
        if not filename.endswith(".mp4"):
            filename = filename.rsplit(".", 1)[0] + ".mp4"

    return filename
