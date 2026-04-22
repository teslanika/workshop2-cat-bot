import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


async def get_random_cat() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(CAT_API_URL) as response:
            data = await response.json()
            return data[0]["url"]


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Напиши мне «какой я сегодня кот» — и я пришлю тебе случайного кота 🐱"
    )


@dp.message(F.text.lower().contains("какой я сегодня кот"))
async def send_cat(message: Message):
    cat_url = await get_random_cat()
    await message.answer_photo(photo=cat_url, caption="Вот твой кот на сегодня 🐾")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
