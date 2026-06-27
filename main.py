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


# -------------------------
# 🔥 OBUNA TEKSHIRISH
# -------------------------
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# -------------------------
# 🔥 OBUNA BUTTON
# -------------------------
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


# -------------------------
# 🔥 START
# -------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    if not await is_subscribed(user_id):
        await message.answer(
            "👋 Salom!\n\n"
            "Botdan foydalanish uchun obuna bo‘ling:\n"
            "📢 Telegram kanal\n📸 Instagram\n\n"
            "Keyin 🔄 Tekshirish bosing.",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer(
        "✅ Obuna tasdiqlandi!\n\n📎 Video link yuboring (YouTube / TikTok / Instagram)"
    )


# -------------------------
# 🔥 CHECK SUB
# -------------------------
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text(
            "✅ Tasdiqlandingiz!\n\n📎 Endi video link yuboring"
        )
    else:
        await callback.answer("❌ Avval obuna bo‘ling!", show_alert=True)


# -------------------------
# 🔥 VIDEO DOWNLOAD
# -------------------------
def download_video(url: str):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bv*+ba/best",   # video + audio
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

        if not file_path.endswith(".mp4"):
            file_path = file_path.rsplit(".", 1)[0] + ".mp4"

    return file_path


# -------------------------
# 🔥 VIDEO HANDLER
# -------------------------
@dp.message()
async def handle_video(message: types.Message):
    url = message.text

    if not url or "http" not in url:
        return

    await message.answer("⬇️ Video yuklanmoqda...\n🎧 Audio qo‘shilmoqda...")

    try:
        file_path = download_video(url)

        await message.answer_video(
            FSInputFile(file_path),
            caption="✅ Tayyor! Video + Audio"
        )

        os.remove(file_path)

    except Exception as e:
        logging.error(e)
        await message.answer("❌ Bu linkdan video yuklab bo‘lmadi")


# -------------------------
# 🔥 MAIN
# -------------------------
async def main():
    logging.info("Bot ishga tushdi...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
