import random
from fastapi import FastAPI, Form, Cookie, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import uuid

app = FastAPI()

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
    # status: 0=start, 1=id_sent, 2=paid, 3=active
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, key TEXT, status INTEGER)')
    conn.commit()
    conn.close()
init_db()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <body style="background:#0a0a0a; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
        <div style="background:#151515; padding:40px; border-radius:30px; max-width:400px; margin:auto;">
            <h1>QUANTUM ANALYTICS</h1>
            <form action="/register" method="post">
                <input name="uid" placeholder="Ваш ID" required style="width:100%; padding:15px; margin-bottom:10px; background:#222; border:none; border-radius:15px; color:white;">
                <button style="width:100%; padding:15px; background:#fff; color:#000; border-radius:15px; cursor:pointer;">РЕГИСТРАЦИЯ</button>
            </form>
        </div>
    </body>
    """

@app.post("/register")
async def register(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (uid, "", 1))
    conn.commit()
    return "<h1>Заявка отправлена. Ожидайте подтверждения ID.</h1>"

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<h1>Админка</h1>"
    for u in users:
        status_text = ["Новый", "ID проверен", "Оплата подтверждена", "Активен"][u[2]]
        html += f"<p>{u[0]} | Статус: {status_text} | "
        if u[2] == 1: html += f"<a href='/set_status/{u[0]}/2'>[ПОДТВЕРДИТЬ ОПЛАТУ]</a>"
        elif u[2] == 2: html += f"<a href='/set_status/{u[0]}/3'>[АКТИВИРОВАТЬ]</a>"
        html += "</p>"
    return html

@app.get("/set_status/{uid}/{status}")
async def set_status(uid: str, status: int):
    conn = sqlite3.connect('users.db')
    key = str(uuid.uuid4())[:8] if status == 3 else ""
    conn.execute('UPDATE users SET status=?, key=? WHERE uid=?', (status, key, uid))
    conn.commit()
    return f"<h1>Статус обновлен. Ключ для входа: {key}</h1>"

@app.post("/login")
async def login(uid: str = Form(...), key: str = Form(...)):
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT * FROM users WHERE uid=? AND key=?', (uid, key)).fetchone()
    if user and user[2] == 3:
        # Здесь будет логика сканера с 45 активами
        return "<h1>ДОСТУП ОТКРЫТ!</h1> <p>Тут будут сигналы...</p>"
    return "<h1>Доступ запрещен.</h1>"
