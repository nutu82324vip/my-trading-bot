from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3, uuid

app = FastAPI()

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
    <html><body style="background:#000; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
        <div style="background:#111; padding:40px; border-radius:30px; max-width:600px; margin:auto;">
            <h1 style="font-size:3rem; color:#00ffcc;">QUANTUM ANALYTICS</h1>
            <p style="font-size:1.5rem;">Профессиональный бот для анализа 45 активов.</p>
            <a href="https://pocket-friends.co/r/vmbewy0x1o" style="font-size:1.5rem; color:#00ffcc;">💎 РЕГИСТРАЦИЯ</a>
            <form action="/register" method="post" style="margin-top:40px;">
                <input name="uid" placeholder="Ваш ID" required style="width:100%; font-size:1.5rem; padding:20px; border-radius:15px; border:none; margin-bottom:20px;">
                <button style="width:100%; font-size:1.5rem; padding:20px; border-radius:15px; border:none; background:#fff;">ОТПРАВИТЬ ID</button>
            </form>
        </div>
    </body></html>
    """

@app.post("/register", response_class=HTMLResponse)
async def register(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (uid, "", 1))
    conn.commit()
    return """<body style="background:#000; color:#fff; text-align:center; padding:50px; font-size:2rem;">
        <h1>ЗАЯВКА ПРИНЯТА</h1>
        <p>Меню ожидания: Изучайте советы, пока мы проверяем ваш статус.</p>
        <ul style="text-align:left; font-size:1.5rem;">
            <li>Риск-менеджмент: 3% на сделку.</li>
            <li>Анализ: 45+ активов в реальном времени.</li>
            <li>Ожидайте активации ключа администратором.</li>
        </ul>
    </body>"""

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#111; color:#fff; padding:50px; font-size:1.5rem;'>"
    html += "<h1>УПРАВЛЕНИЕ</h1>"
    for u in users:
        html += f"<div style='border:1px solid #333; padding:20px; margin-bottom:20px;'>ID: {u[0]} | Статус: {u[2]}<br>"
        html += f"<a href='/set/{u[0]}/2' style='color:#0f0;'>[ПРИНЯТЬ ID]</a> "
        html += f"<a href='/set/{u[0]}/3' style='color:#0ff;'>[АКТИВИРОВАТЬ]</a> "
        html += f"<a href='/set/{u[0]}/cancel' style='color:#f00;'>[ОТМЕНИТЬ]</a></div>"
    return html + "</body>"

@app.get("/set/{uid}/{action}", response_class=HTMLResponse)
async def set_status(uid: str, action: str):
    conn = sqlite3.connect('users.db')
    if action == "2": conn.execute('UPDATE users SET status=2 WHERE uid=?', (uid,))
    elif action == "3": conn.execute('UPDATE users SET status=3, key=? WHERE uid=?', (str(uuid.uuid4())[:8], uid))
    elif action == "cancel": conn.execute('DELETE FROM users WHERE uid=?', (uid,))
    conn.commit()
    return "<h1>ДЕЙСТВИЕ ВЫПОЛНЕНО</h1><a href='/admin'>НАЗАД</a>"
