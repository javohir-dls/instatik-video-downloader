import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Instagramga obuna bo‘lish",
                url="https://instagram.com/javohir.ftbl"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Javohirbekning InstaTik Video Downloader boti ishlayapti ✅\n\n"
        "📌 Bot hozir faol holatda\n"
        "📥 Video yuklash funksiyasi tez orada qo‘shiladi\n\n"
        "👉 Davom etish uchun Instagramga obuna bo‘ling",
        reply_markup=reply_markup
    )


# 🔥 MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot ishlayapti...")

    app.run_polling()


if __name__ == "__main__":
    main()
