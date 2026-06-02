import random
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Все 45 активов Pocket Option
ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "NZD/USD", "AUD/JPY", "CHF/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC", "NZD/USD OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "LTC/USDT", "ADA/USDT", "DOT/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC", "DOGE/USDT OTC",
    "Apple", "Tesla", "NVIDIA", "Amazon", "Microsoft", "Google", "Netflix", "Meta",
    "Apple OTC", "Tesla OTC", "NVIDIA OTC", "Amazon OTC", "Gold"
]

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, status TEXT)')
    conn.commit()
    conn.close()
init_db()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html style="height:100%;"><body style="background:#0a0a0a; color:#fff; font-family:'Segoe UI', sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0;">
        <div style="background:#151515; padding:40px; border-radius:30px; box-shadow:0 10px 30px rgba(0,0,0,0.5); width:90%; max-width:500px; text-align:center;">
            <h1 style="color:#fff;">QUANTUM ANALYTICS</h1>
            <p style="color:#888;">Система анализа финансовых рынков</p>
            <form action="/login" method="post">
                <input name="uid" placeholder="Ваш ID" required style="width:100%; padding:15px; background:#222; border:none; border-radius:15px; color:white; margin-bottom:15px; box-sizing:border-box;">
                <button style="width:100%; padding:15px; background:#fff; color:#000; border:none; border-radius:15px; font-weight:bold; cursor:pointer;">ВОЙТИ</button>
            </form>
        </div>
    </body></html>
    """

@app.post("/login", response_class=HTMLResponse)
async def login(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?)', (uid, 'pending'))
    conn.commit()
    return """
    <body style="background:#0a0a0a; color:#fff; font-family:sans-serif; text-align:center; padding-top:50px;">
        <div style="background:#151515; padding:40px; border-radius:30px; display:inline-block; max-width:400px;">
            <h2>Статус: Ожидание</h2>
            <p style="color:#888;">Ваша заявка принята. Ожидайте активации администратором.</p>
            <ul style="text-align:left; color:#ccc;">
                <li>Следите за рисками: не более 3% на сделку.</li>
                <li>Используйте перекрытия только по рекомендации.</li>
                <li>Система анализирует 45+ активов в реальном времени.</li>
            </ul>
        </div>
    </body>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#111; color:#fff; padding:30px; font-family:sans-serif;'><h1>Управление доступом</h1>"
    for u in users:
        html += f"<div style='background:#222; padding:15px; border-radius:15px; margin-bottom:10px;'>ID: {u[0]} | Статус: {u[1]} <a href='/approve/{u[0]}' style='color:#0f0; margin-left:20px; font-weight:bold;'>[ОК - АКТИВИРОВАТЬ]</a></div>"
    return html + "</body>"

@app.get("/approve/{uid}")
async def approve(uid: str):
    conn = sqlite3.connect('users.db')
    conn.execute('UPDATE users SET status=? WHERE uid=?', ('active', uid))
    conn.commit()
    return "<h1 style='color:white; font-family:sans-serif;'>Пользователь успешно активирован!</h1>"
