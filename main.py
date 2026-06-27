import asyncio
import os
import yt_dlp

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_TOKEN


# 📥 video yuklab olish funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# 🚀 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Kanalga obuna",
                url="https://instagram.com/javohir.ftbl"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎬 InstaTik Video Bot\n\n"
        "📥 Video link yuboring (YouTube/TikTok)\n"
        "⚡ Men yuklab beraman",
        reply_markup=reply_markup
    )


# 📥 video handler
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Yuklanmoqda...")

    try:
        download_video(url)

        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video=video)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")


# 🔥 botni ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
