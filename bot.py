import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Вставьте токен строго в одну строку без переносов
API_TOKEN = '8601317051:AAEBAVaHTZ9VM25bOFsIPICi8IC3mfKiEzQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот успешно запущен и работает!")

async def main():
    print("--- БОТ ЗАПУЩЕН ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
