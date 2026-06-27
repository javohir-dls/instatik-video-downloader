import os
print("SCRIPT STARTED")

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8787348134:AAFNAot8sCUcXfvibh-4kDrHjzRAWu2u5jQ")

print("TOKEN =", BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START TRIGGERED")
    await update.message.reply_text("OK ISHLAYAPTI")

def main():
    print("BOT STARTING...")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
