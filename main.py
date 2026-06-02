import random
from fastapi import FastAPI, Form, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, key TEXT, status TEXT)')
    conn.commit()
    conn.close()
init_db()

ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "NZD/USD", "AUD/JPY", "CHF/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC", "NZD/USD OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "LTC/USDT", "ADA/USDT", "DOT/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC", "DOGE/USDT OTC",
    "Apple", "Tesla", "NVIDIA", "Amazon", "Microsoft", "Google", "Netflix", "Meta",
    "Apple OTC", "Tesla OTC", "NVIDIA OTC", "Amazon OTC", "Gold"
]

@app.get("/", response_class=HTMLResponse)
async def home(user_key: str = Cookie(None)):
    if user_key:
        conn = sqlite3.connect('users.db')
        user = conn.execute('SELECT * FROM users WHERE key=?', (user_key,)).fetchone()
        if user and user[2] == 'active':
            return "<h1>ДОБРО ПОЖАЛОВАТЬ В ТЕРМИНАЛ</h1>"
    
    return """
    <body style="background:#0a0a0a; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
        <div style="background:#151515; padding:40px; border-radius:30px; max-width:400px; margin:auto;">
            <h1>ВХОД В QUANTUM</h1>
            <form action="/login" method="post">
                <input name="uid" placeholder="Ваш ID" required style="width:100%; padding:15px; background:#222; border:none; border-radius:15px; color:white; margin-bottom:10px;">
                <input name="key" placeholder="Ваш Ключ" required style="width:100%; padding:15px; background:#222; border:none; border-radius:15px; color:white; margin-bottom:10px;">
                <button style="width:100%; padding:15px; background:#fff; color:#000; border-radius:15px; cursor:pointer;">ВОЙТИ</button>
            </form>
        </div>
    </body>
    """

@app.post("/login")
async def login(uid: str = Form(...), key: str = Form(...)):
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT status FROM users WHERE uid=? AND key=?', (uid, key)).fetchone()
    if user and user[0] == 'active':
        response = RedirectResponse(url="/scanner")
        response.set_cookie(key="user_key", value=key)
        return response
    return "<h1>Ошибка: Неверные данные или доступ закрыт.</h1>"

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<h1>Админка</h1>"
    for u in users:
        html += f"<p>{u[0]} | Статус: {u[2]} <a href='/approve/{u[0]}'>[АКТИВИРОВАТЬ]</a></p>"
    return html

@app.get("/approve/{uid}")
async def approve(uid: str):
    conn = sqlite3.connect('users.db')
    conn.execute('UPDATE users SET status=? WHERE uid=?', ('active', uid))
    conn.commit()
    return "<h1>Активировано!</h1>"

