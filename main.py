from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 @javohir.ftbl ga obuna bo'lish",
                url="https://instagram.com/javohir.ftbl"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎬 InstaTik Video Downloader\n\n"
        "📥 Instagram, TikTok yoki YouTube Shorts havolasini yuboring.\n\n"
        "⚡ Men videoni yuklab beraman.",
        reply_markup=reply_markup,
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏳ Havola qabul qilindi.\n"
        "🔧 Video yuklab olinmoqda..."
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("✅ Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
