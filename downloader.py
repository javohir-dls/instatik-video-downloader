import os
import uuid
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_video(url: str, audio=False):
    file_id = str(uuid.uuid4())[:8]
    output = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    ydl_opts = {"outtmpl": output}

    if audio:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = ydl.prepare_filename(info)

    if audio:
        path = path.rsplit(".", 1)[0] + ".mp3"

    return path
