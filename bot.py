import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = '8601317051:AAFEL24P_6WFdJfvtL3Ts1VQeVXuxjmKFr8'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот ответил!")

async def main():
    print("--- БОТ СТАЛ ТУТ И ЖДЕТ СООБЩЕНИЙ ---")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"--- КРИТИЧЕСКАЯ ОШИБКА: {e} ---")

if __name__ == "__main__":
    asyncio.run(main())
