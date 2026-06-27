from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Obuna", url="https://instagram.com/javohir.ftbl")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🎬 Bot ishlayapti", reply_markup=reply_markup)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Yuklanmoqda...")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
