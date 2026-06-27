import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Obuna", url="https://instagram.com/javohir.ftbl")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🎬 Bot ishlayapti", reply_markup=reply_markup)

import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': '/tmp/video.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Video yuklanmoqda...")

    try:
        download_video(url)
        await update.message.reply_video(video=open("/tmp/video.mp4", "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot started")

    # 🔥 CRITICAL FIX FOR RENDER + PYTHON 3.14
    asyncio.set_event_loop(asyncio.new_event_loop())

    app.run_polling()

if __name__ == "__main__":
    main()
