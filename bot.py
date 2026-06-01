import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiohttp import web

# Ваши данные
API_TOKEN = '8116004627:AAFhHQGrXO5bD21t41XiKB-YbLLQeGqO15c'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message):
    await message.answer("Бот успешно запущен и работает!")

# Функция для веб-сервера
async def web_handler(request):
    return web.Response(text="Bot is running")

async def run_web():
    app = web.Application()
    app.router.add_get('/', web_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render передает PORT через переменную окружения
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    await asyncio.Event().wait() # Держим сервер запущенным

async def main():
    # Запускаем и сервер, и бота параллельно
    await asyncio.gather(run_web(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
