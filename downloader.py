import os
import yt_dlp


def download_video(url):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title).80s.%(ext)s",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if info is None:
                return None

            filename = ydl.prepare_filename(info)

            base = os.path.splitext(filename)[0]

            for ext in [".mp4", ".mkv", ".webm", ".mov"]:
                if os.path.exists(base + ext):
                    return base + ext

            if os.path.exists(filename):
                return filename

            return None

    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        return None
