import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Ваши данные
API_TOKEN = '8116004627:AAFhHQGrXO5bD21t41XiKB-YbLLQeGqO15c'
ADMIN_ID = 1883817844

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот работает!")

# Это нужно для Render, чтобы он не убивал бота
async def handle(request):
    return web.Response(text="Bot is running")

async def run_bot():
    await dp.start_polling(bot)

async def run_web():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await asyncio.gather(run_web(), run_bot())

if __name__ == "__main__":
    asyncio.run(main())
