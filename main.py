import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from downloader import download_video
from config import TOKEN, CHANNEL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ---------------- OBUNA ----------------
async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📢 Telegram", url=f"https://t.me/{CHANNEL.replace('@','')}")],
        [InlineKeyboardButton("📸 Instagram", url="https://instagram.com/javohir.ftbl")],
        [InlineKeyboardButton("🔄 Tekshirish", callback_data="check")]
    ])


# ---------------- START ----------------
@dp.message(CommandStart())
async def start(message: types.Message):

    if not await is_subscribed(message.from_user.id):
        await message.answer(
            "📢 Avval obuna bo‘ling:",
            reply_markup=sub_keyboard()
        )
        return

    await message.answer("📎 Video link yuboring")


# ---------------- CHECK ----------------
@dp.callback_query(F.data == "check")
async def check(call: types.CallbackQuery):

    if await is_subscribed(call.from_user.id):
        await call.message.edit_text("📎 Endi video link yuboring")
    else:
        await call.answer("❌ Obuna yo‘q", show_alert=True)


# ---------------- VIDEO HANDLER ----------------
@dp.message(F.text)
async def handle(message: types.Message):

    url = message.text

    if "http" not in url:
        return

    await message.answer("⬇️ Yuklanmoqda...")

    try:
        file_path = download_video(url)

        if not file_path:
            await message.answer("❌ Video topilmadi")
            return

        await message.answer_video(
            FSInputFile(file_path),
            caption="✅ MP4 tayyor"
        )

        os.remove(file_path)

    except Exception as e:
        logging.exception(e)
        await message.answer("❌ Yuklab bo‘lmadi")


# ---------------- MAIN ----------------
async def main():
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
