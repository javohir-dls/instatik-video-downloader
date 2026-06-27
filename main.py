import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# logging (Render debug uchun juda muhim)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Instagramga obuna bo‘lish",
                url="https://instagram.com/javohir.ftbl"
            )
        ]
    ]

    await update.message.reply_text(
        "🎬 *InstaTik Downloader Bot*\n\n"
        "📥 Instagram / TikTok / YouTube Shorts link yuboring\n"
        "⚡ Men videoni yuklab beraman",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# link qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "http" in text:
        await update.message.reply_text(
            "⏳ Video yuklanmoqda...\nTez orada tayyor bo‘ladi"
        )
    else:
        await update.message.reply_text(
            "❗ Iltimos faqat video link yuboring"
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi!")

    print("BOT STARTED")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
