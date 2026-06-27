import asyncio
import os
import yt_dlp

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_TOKEN


# 📥 video yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "video.mp4",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Obuna bo‘lish",
                url="https://instagram.com/javohir.ftbl"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Javohirbekning InstaTik Video Downloader boti\n\n"
        "📥 Instagram / TikTok / YouTube link yuboring\n"
        "⚡ Men videoni yuklab beraman\n\n"
        "👉 Davom etish uchun obuna bo‘ling",
        reply_markup=reply_markup
    )


# 📥 video handler
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Video yuklanmoqda...")

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_video, url)

        if not os.path.exists("video.mp4"):
            await update.message.reply_text("❌ Video topilmadi yoki link ishlamaydi")
            return

        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video=video)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")


# 🔥 main
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Javohirbek bot ishlayapti...")

    app.run_polling()


if __name__ == "__main__":
    main()
