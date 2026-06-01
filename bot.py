import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# ВСТАВЬТЕ ТОКЕН СЮДА БЕЗ ПРОБЕЛОВ
TOKEN = '8601317051:AAFEL24P_6WFdJfvtL3Ts1VQeVXuxjmKFr8'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот работает!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
