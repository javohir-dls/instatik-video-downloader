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

# saqlangan video path
user_files = {}


# ---------------- OBUNA ----------------
async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def sub_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📢 Kanal", url="https://t.me/xushboqovblog")],
        [InlineKeyboardButton("📸 Instagram", url="https://instagram.com/javohir.ftbl")],
        [InlineKeyboardButton("🔄 Tekshirish", callback_data="check")]
    ])


# ---------------- DOWNLOAD ----------------
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


def extract_audio(video_path: str):
    audio_path = video_path.replace(".mp4", ".mp3")

    os.system(f'ffmpeg -y -i "{video_path}" -q:a 0 -map a "{audio_path}"')

    return audio_path


# ---------------- START ----------------
@dp.message(CommandStart())
async def start(msg: types.Message):
    if not await is_subscribed(msg.from_user.id):
        await msg.answer("📢 Avval obuna bo‘ling", reply_markup=sub_kb())
        return

    await msg.answer("📎 Video link yuboring")


# ---------------- CHECK ----------------
@dp.callback_query(F.data == "check")
async def check(cb: types.CallbackQuery):
    if await is_subscribed(cb.from_user.id):
        await cb.message.edit_text("📎 Endi link yuboring")
    else:
        await cb.answer("❌ Obuna yo‘q", show_alert=True)


# ---------------- VIDEO ----------------
@dp.message(F.text)
async def handle(msg: types.Message):
    url = msg.text

    if "http" not in url:
        return

    await msg.answer("⬇️ Yuklanmoqda...")

    try:
        video = download_video(url)

        user_files[msg.from_user.id] = video

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🎵 MP3 olish", callback_data="mp3")]
        ])

        await msg.answer_video(
            FSInputFile(video),
            caption="✅ MP4 tayyor",
            reply_markup=kb
        )

    except Exception as e:
        logging.error(e)
        await msg.answer("❌ Yuklab bo‘lmadi")


# ---------------- MP3 ----------------
@dp.callback_query(F.data == "mp3")
async def mp3(cb: types.CallbackQuery):
    uid = cb.from_user.id

    if uid not in user_files:
        await cb.answer("❌ Avval video yuboring", show_alert=True)
        return

    video_path = user_files[uid]

    await cb.message.answer("🎵 MP3 tayyorlanmoqda...")

    try:
        audio_path = extract_audio(video_path)

        await cb.message.answer_audio(
            FSInputFile(audio_path),
            caption="🎧 Faqat musiqa"
        )

    except Exception as e:
        logging.error(e)
        await cb.message.answer("❌ MP3 qilib bo‘lmadi")


# ---------------- MAIN ----------------
async def main():
    logging.info("Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
