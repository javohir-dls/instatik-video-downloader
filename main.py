import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN, CHANNEL_ID, INSTAGRAM_URL
from downloader import download_video

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# ================= KEYBOARDS =================
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Telegram kanal", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")],
        [InlineKeyboardButton(text="📸 Instagram", url=INSTAGRAM_URL)],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")]
    ])


def download_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 MP4", callback_data="mp4")],
        [InlineKeyboardButton(text="🎵 MP3", callback_data="mp3")]
    ])


# ================= CHECK SUB =================
async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ================= START =================
@router.message(CommandStart())
async def start(msg: Message):
    await msg.answer(
        "👋 Salom!\n"
        "Botdan foydalanish uchun kanalga obuna bo‘ling:",
        reply_markup=start_kb()
    )


# ================= CHECK BUTTON =================
@router.callback_query(F.data == "check")
async def check(call: CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.answer("✅ Tasdiqlandi! Endi link yuboring 🚀")
    else:
        await call.message.answer("❌ Avval kanalga obuna bo‘ling!")


# ================= LINK HANDLER (FIXED) =================
@router.message()
async def handle(msg: Message):
    text = msg.text

    if not text:
        return

    if "http" in text:
        await msg.answer("⏳ Yuklanmoqda...")

        try:
            # 🔥 SAFE DOWNLOAD (osilib qolmaydi)
            file_path = await asyncio.wait_for(
                asyncio.to_thread(download_video, text),
                timeout=60
            )

            with open(file_path, "rb") as video:
                await msg.answer_document(
                    video,
                    caption="✅ Tayyor video",
                    reply_markup=download_kb()
                )

        except asyncio.TimeoutError:
            await msg.answer("❌ Download juda uzoq davom etdi")
        except Exception as e:
            await msg.answer(f"❌ Xatolik: {e}")

    else:
        await msg.answer("⚠️ Faqat link yuboring")


# ================= MP3 =================
@router.callback_query(F.data == "mp3")
async def mp3(call: CallbackQuery):
    await call.message.answer("🎵 MP3 funksiyasi keyingi update da ulanadi")


# ================= MP4 =================
@router.callback_query(F.data == "mp4")
async def mp4(call: CallbackQuery):
    await call.message.answer("🎬 Video allaqachon yuborilgan")


# ================= START BOT =================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
