import asyncio
import logging
import os
import yt_dlp

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@xushboqovblog"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}


# ---------------- CHECK SUB ----------------
async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---------------- START KEYBOARD ----------------
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📢 Telegram kanal", url="https://t.me/xushboqovblog")],
        [InlineKeyboardButton("📸 Instagram", url="https://instagram.com/javohir.ftbl")],
        [InlineKeyboardButton("🔄 Tekshirish", callback_data="check")]
    ])


# ---------------- DOWNLOAD VIDEO ----------------
def download_video(url: str):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path


# ---------------- MP3 EXTRACT ----------------
def extract_audio(video_path: str):
    audio_path = video_path.rsplit(".", 1)[0] + ".mp3"
    os.system(f'ffmpeg -y -i "{video_path}" -q:a 0 -map a "{audio_path}"')
    return audio_path


# ---------------- START ----------------
@dp.message(CommandStart())
async def start(message: types.Message):

    if not await is_subscribed(message.from_user.id):
        await message.answer(
            "👋 Salom!\n\n📢 Botdan foydalanish uchun obuna bo‘ling:",
            reply_markup=start_kb()
        )
        return

    await message.answer("📎 Video link yuboring")


# ---------------- CHECK BUTTON ----------------
@dp.callback_query(F.data == "check")
async def check(call: types.CallbackQuery):

    if await is_subscribed(call.from_user.id):
        await call.message.edit_text("📎 Endi video link yuboring")
    else:
        await call.answer("❌ Avval obuna bo‘ling", show_alert=True)


# ---------------- HANDLE VIDEO LINK ----------------
@dp.message(F.text)
async def handle(message: types.Message):

    url = message.text

    if "http" not in url:
        return

    await message.answer("⬇️ Video yuklanmoqda...")

    try:
        video = download_video(url)

        user_data[message.from_user.id] = video

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🎵 MP3 olish", callback_data="mp3")]
        ])

        await message.answer_video(
            FSInputFile(video),
            caption="✅ MP4 tayyor",
            reply_markup=kb
        )

    except Exception as e:
        logging.error(e)
        await message.answer("❌ Yuklab bo‘lmadi")


# ---------------- MP3 BUTTON ----------------
@dp.callback_query(F.data == "mp3")
async def mp3(call: types.CallbackQuery):

    uid = call.from_user.id

    if uid not in user_data:
        await call.answer("❌ Avval video yuboring", show_alert=True)
        return

    video_path = user_data[uid]

    await call.message.answer("🎵 MP3 tayyorlanmoqda...")

    try:
        audio = extract_audio(video_path)

        await call.message.answer_audio(
            FSInputFile(audio),
            caption="🎧 Musiqa"
        )

    except Exception as e:
        logging.error(e)
        await call.message.answer("❌ MP3 qilib bo‘lmadi")


# ---------------- MAIN ----------------
async def main():
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
