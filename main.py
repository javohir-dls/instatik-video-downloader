import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from downloader import download_file

# logging
logging.basicConfig(level=logging.INFO)

# bot + dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)


# /start
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Salom!\n"
        "Menga video yoki file link yuboring, men yuklab beraman 🚀"
    )


# umumiy handler
@router.message()
async def message_handler(message: Message):
    text = message.text

    if not text:
        await message.answer("❌ Faqat link yuboring")
        return

    if text.startswith("http"):
        await message.answer("⏳ Yuklanmoqda...")

        try:
            file_path = await download_file(text)

            await message.answer_document(
                document=open(file_path, "rb"),
                caption="✅ Tayyor!"
            )

        except Exception as e:
            await message.answer(f"❌ Xatolik: {e}")
    else:
        await message.answer("⚠️ Iltimos, http/https link yuboring")


# bot ishga tushirish
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
