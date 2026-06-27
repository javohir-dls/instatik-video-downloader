import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START ISHLADI")
    await update.message.reply_text("OK ishlayapti")

def main():
    print("BOT STARTED")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
