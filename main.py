import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL = "@xushboqovblog"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# kanalni tekshirish funksiyasi
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        status = member.status
        return status in ["member", "administrator", "creator"]
    except:
        return False


# obuna tugmasi
def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url=f"https://t.me/{CHANNEL.replace('@','')}"
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


# social media tugmalar
def social_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/javohir.ftbl"),
            ],
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


@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    if not await is_subscribed(user_id):
        await message.answer(
            "❗ Botdan foydalanish uchun avval kanalga obuna bo‘ling:",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer(
        "✅ Xush kelibsiz!\nQuyidagi videolarni ochishingiz mumkin:",
        reply_markup=social_keyboard()
    )


@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if await is_subscribed(user_id):
        await callback.message.edit_text(
            "✅ Obuna tasdiqlandi!\nEndi videolarni ochishingiz mumkin:",
            reply_markup=social_keyboard()
        )
    else:
        await callback.answer("❌ Siz hali kanalga obuna bo‘lmagansiz!", show_alert=True)


async def main():
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
