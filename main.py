from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import sqlite3, uuid

app = FastAPI()

# Все 45 активов
ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "NZD/USD", "AUD/JPY", "CHF/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC", "NZD/USD OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "LTC/USDT", "ADA/USDT", "DOT/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC", "DOGE/USDT OTC",
    "Apple", "Tesla", "NVIDIA", "Amazon", "Microsoft", "Google", "Netflix", "Meta",
    "Apple OTC", "Tesla OTC", "NVIDIA OTC", "Amazon OTC", "Gold", "Silver", "Brent Oil"
]

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, key TEXT, status INTEGER)')
    conn.commit()
    conn.close()
init_db()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="font-size: 20px;"><body style="background:#000; color:#fff; font-family:sans-serif; text-align:center; padding:40px;">
        <div style="background:#111; padding:50px; border-radius:30px; max-width:700px; margin:auto; border: 2px solid #333;">
            <h1 style="font-size: 3.5rem; color:#00ffcc;">QUANTUM ANALYTICS</h1>
            <p style="font-size: 1.6rem; color:#ccc; line-height: 1.6;">Профессиональный анализатор рынков. Доступно 45+ активов в режиме реального времени.</p>
            <br>
            <a href="https://pocket-friends.co/r/vmbewy0x1o" style="font-size: 1.6rem; color:#00ffcc; text-decoration:none;">💎 РЕГИСТРАЦИЯ (ОБЯЗАТЕЛЬНО)</a>
            <form action="/register" method="post" style="margin-top:40px;">
                <input name="uid" placeholder="Введите ваш ID" required style="width:100%; font-size: 1.6rem; padding:25px; border-radius:15px; border:none; background:#222; color:white; margin-bottom:20px; box-sizing:border-box;">
                <button style="width:100%; font-size: 1.6rem; padding:25px; border-radius:15px; border:none; background:#fff; font-weight:bold; cursor:pointer;">ОТПРАВИТЬ ID</button>
            </form>
        </div>
    </body></html>
    """

@app.post("/register")
async def register(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (uid, "", 1))
    conn.commit()
    return """<body style="background:#000; color:#fff; padding:60px; text-align:center; font-size: 2.2rem;">
        <h1>Заявка принята!</h1>
        <p>Ваш ID в очереди на проверку.<br>Соблюдайте риск-менеджмент: не более 3% на сделку.</p>
    </body>"""

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#111; color:#fff; padding:50px; font-size: 1.6rem;'>"
    html += "<h1 style='font-size: 3rem;'>УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ</h1>"
    for u in users:
        html += f"<div style='background:#222; padding:30px; border-radius:20px; margin-bottom:20px;'>ID: {u[0]} | Статус: {u[2]}<br>"
        html += f"<a href='/action/{u[0]}/2' style='color:#0f0; margin-right:30px;'>[ПРИНЯТЬ ID]</a>"
        html += f"<a href='/action/{u[0]}/3' style='color:#0ff; margin-right:30px;'>[АКТИВИРОВАТЬ]</a>"
        html += f"<a href='/action/{u[0]}/cancel' style='color:#f00;'>[ОТМЕНИТЬ]</a></div>"
    return html + "</body>"

@app.get("/action/{uid}/{action}")
async def action(uid: str, action: str):
    conn = sqlite3.connect('users.db')
    if action == "2": conn.execute('UPDATE users SET status=2 WHERE uid=?', (uid,))
    elif action == "3": conn.execute('UPDATE users SET status=3, key=? WHERE uid=?', (str(uuid.uuid4())[:8], uid))
    elif action == "cancel": conn.execute('DELETE FROM users WHERE uid=?', (uid,))
    conn.commit()
    return "<h1 style='font-size:2rem; padding:50px;'>ДЕЙСТВИЕ ВЫПОЛНЕНО. <a href='/admin'>НАЗАД</a></h1>"
