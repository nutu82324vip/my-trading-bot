from fastapi import FastAPI, Form, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3, uuid

app = FastAPI()

# Список из 45 активов
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
    # Статусы: 1=Регистрация, 2=Ждет подтверждения оплаты, 3=Активен
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, key TEXT, status INTEGER)')
    conn.commit()
    conn.close()
init_db()

@app.get("/", response_class=HTMLResponse)
async def index(uid: str = Cookie(None)):
    if uid:
        conn = sqlite3.connect('users.db')
        user = conn.execute('SELECT status, key FROM users WHERE uid=?', (uid,)).fetchone()
        if user:
            if user[0] == 3: # Активен - ПОКАЗЫВАЕМ СКАНИРОВАНИЕ
                opts = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
                return f"""<body style="background:#050505; color:#fff; font-family:sans-serif; padding:40px; text-align:center;">
                    <h1>QUANTUM SCANNER</h1>
                    <select style="width:100%; padding:20px; font-size:1.5rem;">{opts}</select>
                    <button style="width:100%; padding:20px; font-size:1.5rem; margin-top:20px;">ЗАПУСТИТЬ ИИ АНАЛИЗ</button>
                    <p>Поддержка: t.me/ваш_тг | email@mail.com</p>
                </body>"""
            return "<body style='background:#050505; color:#fff; padding:40px; text-align:center;'><h1>ОЖИДАНИЕ...</h1><p>Ваша заявка на рассмотрении.</p></body>"

    return """<body style="background:#050505; color:#fff; font-family:sans-serif; padding:40px; text-align:center;">
        <h1>QUANTUM ACCESS</h1>
        <form action="/register" method="post">
            <input name="uid" placeholder="Ваш ID" style="width:100%; padding:20px; font-size:1.5rem; border-radius:15px; margin-bottom:20px;">
            <button style="width:100%; padding:20px; font-size:1.5rem; border-radius:15px; background:#fff;">РЕГИСТРАЦИЯ</button>
        </form>
    </body>"""

@app.post("/register")
async def register(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (uid, "", 1))
    conn.commit()
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="uid", value=uid)
    return response

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#111; color:#fff; font-family:sans-serif; padding:40px;'>"
    for u in users:
        html += f"<div style='border:1px solid #444; padding:20px; margin-bottom:20px;'>ID: {u[0]} | Status: {u[2]}<br>"
        html += f"<a href='/set/{u[0]}/2'>[ПОДТВЕРДИТЬ ID]</a> <a href='/set/{u[0]}/3'>[АКТИВИРОВАТЬ]</a> <a href='/set/{u[0]}/del'>[УДАЛИТЬ]</a></div>"
    return html + "</body>"

@app.get("/set/{uid}/{action}")
async def set_status(uid: str, action: str):
    conn = sqlite3.connect('users.db')
    if action == "2": conn.execute('UPDATE users SET status=2 WHERE uid=?', (uid,))
    elif action == "3": conn.execute('UPDATE users SET status=3, key=? WHERE uid=?', (str(uuid.uuid4())[:8], uid))
    elif action == "del": conn.execute('DELETE FROM users WHERE uid=?', (uid,))
    conn.commit()
    return "<h1>СТАТУС ОБНОВЛЕН. <a href='/admin'>НАЗАД</a></h1>"
