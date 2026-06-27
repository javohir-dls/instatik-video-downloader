import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Javohirbekni InstaTik boti ishlayapti ✅")

def main():
    print("BOT STARTED")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 🔥 MUHIM: run_polling oddiy ishlatamiz
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
