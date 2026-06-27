from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN

def start(update, context):
    keyboard = [[InlineKeyboardButton("📢 Obuna", url="https://instagram.com/javohir.ftbl")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Bot ishlayapti", reply_markup=reply_markup)

def download(update, context):
    update.message.reply_text("⏳ Yuklanmoqda...")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download))

    print("Bot started")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
