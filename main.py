import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@xushboqovblog"

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# 🔥 kanal tekshirish
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🔥 subscribe keyboard
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


# 🔥 video / social keyboard
def social_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/javohir.ftbl")],
            [
                InlineKeyboardButton(text="🎵 TikTok", url="https://tiktok.com"),
                InlineKeyboardButton(text="▶️ YouTube", url="https://youtube.com"),
            ],
            [
                InlineKeyboardButton(text="👻 Snapchat", url="https://snapchat.com"),
                InlineKeyboardButton(text="📘 Facebook", url="https://facebook.com"),
            ]
        ]
    )


# 🔥 start
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    if not await is_subscribed(user_id):
        await message.answer(
            "👋 Salom!\n\n"
            "Botdan foydalanish uchun obuna bo‘ling:\n\n"
            "📢 Telegram kanal\n"
            "📸 Instagram\n\n"
            "Keyin 🔄 Tekshirish bosing.",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer(
        "✅ Obuna tasdiqlandi!\n\n"
        "🎬 Endi video havola yuboring:"
    )


# 🔥 check subscription
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if await is_subscribed(user_id):
        await callback.message.edit_text(
            "✅ Tasdiqlandingiz!\n\n🎬 Endi video link yuboring."
        )
    else:
        await callback.answer(
            "❌ Avval kanalga obuna bo‘ling!",
            show_alert=True
        )


# 🔥 video handler
@dp.message()
async def video_handler(message: types.Message):
    if "http" in (message.text or ""):
        await message.answer(
            "🎬 Video qabul qilindi!\n\n"
            f"📎 Link: {message.text}"
        )


# 🔥 main
async def main():
    logging.info("Bot ishga tushdi...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
