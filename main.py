import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@xushboqovblog"

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ----------------------------
# 🔥 OBUNA TEKSHIRISH
# ----------------------------
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ----------------------------
# 🔥 OBUNA KEYBOARD
# ----------------------------
def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Telegram kanal",
                    url="https://t.me/xushboqovblog"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📸 Instagram",
                    url="https://instagram.com/javohir.ftbl"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Tekshirish",
                    callback_data="check_sub"
                )
            ]
        ]
    )


# ----------------------------
# 🔥 START
# ----------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    if not await is_subscribed(user_id):
        await message.answer(
            "👋 Salom!\n\n"
            "Botdan foydalanish uchun obuna bo‘ling:\n\n"
            "📢 Telegram kanal\n📸 Instagram\n\n"
            "Keyin 🔄 Tekshirish bosing.",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer(
        "✅ Obuna tasdiqlandi!\n\n"
        "📎 Endi video link yuboring (Instagram / TikTok / YouTube)"
    )


# ----------------------------
# 🔥 CHECK SUB
# ----------------------------
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if await is_subscribed(user_id):
        await callback.message.edit_text(
            "✅ Tasdiqlandingiz!\n\n📎 Endi video link yuboring"
        )
    else:
        await callback.answer("❌ Avval obuna bo‘ling!", show_alert=True)


# ----------------------------
# 🔥 VIDEO DOWNLOAD FUNCTION
# ----------------------------
def download_video(url: str):
    ydl_opts = {
        "outtmpl": "video.mp4",
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "video.mp4"


# ----------------------------
# 🔥 VIDEO HANDLER
# ----------------------------
@dp.message()
async def handle_video(message: types.Message):
    url = message.text

    if not url or "http" not in url:
        return

    await message.answer("⬇️ Video yuklanmoqda...")

    try:
        file_path = download_video(url)

        await message.answer_video(
            FSInputFile(file_path),
            caption="✅ Tayyor!"
        )

        os.remove(file_path)

    except Exception as e:
        await message.answer("❌ Bu linkdan video yuklab bo‘lmadi")
        logging.error(e)


# ----------------------------
# 🔥 MAIN
# ----------------------------
async def main():
    logging.info("Bot ishga tushdi...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
