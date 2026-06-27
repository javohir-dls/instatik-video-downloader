import yt_dlp
import os

def download_video(url):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


async def download(update, context):
    url = update.message.text

    await update.message.reply_text("⏳ Yuklanmoqda...")

    try:
        download_video(url)

        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video=video)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")
