from fastapi import FastAPI, Form, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
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

# --- ЛЕНДИНГ ---
@app.get("/", response_class=HTMLResponse)
async def index(uid: str = Cookie(None)):
    if uid:
        conn = sqlite3.connect('users.db')
        user = conn.execute('SELECT status, key FROM users WHERE uid=?', (uid,)).fetchone()
        if user:
            if user[0] == 3: # Доступ открыт
                options = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
                return f"<body style='background:#000; color:#fff; padding:50px; text-align:center;'><h1>СИСТЕМА АКТИВНА</h1><select style='font-size:1.5rem;'>{options}</select><br><br><button style='padding:20px; font-size:1.5rem;' onclick='location.reload()'>ЗАПУСТИТЬ АНАЛИЗ</button></body>"
            return f"<body style='background:#000; color:#fff; padding:50px; text-align:center; font-size:1.5rem;'><h1>МЕНЮ ОЖИДАНИЯ</h1><p>Советов: Не более 3% на сделку, анализируйте новости.</p></body>"
    
    return """<body style="background:#000; color:#fff; text-align:center; padding:50px; font-size:1.5rem;">
        <div style="background:#111; padding:40px; border-radius:30px;"><h1>QUANTUM</h1><form action="/login" method="post"><input name="uid" style="padding:20px; font-size:1.5rem; width:80%;" placeholder="Введите ваш ID"><button style="padding:20px; font-size:1.5rem;">ВОЙТИ</button></form></div>
    </body>"""

@app.post("/login")
async def login(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (uid, "", 1))
    conn.commit()
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="uid", value=uid)
    return response

# --- АДМИНКА ---
@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#111; color:#fff; padding:50px; font-size:1.5rem;'>"
    for u in users:
        html += f"<div style='border:2px solid #333; padding:20px; margin-bottom:20px;'>ID: {u[0]} | Статус: {u[2]}<br>"
        html += f"<a href='/set/{u[0]}/2' style='color:#0f0;'>[ПРИНЯТЬ ID]</a> <a href='/set/{u[0]}/3' style='color:#0ff;'>[АКТИВИРОВАТЬ]</a> <a href='/set/{u[0]}/cancel' style='color:#f00;'>[ОТМЕНИТЬ]</a></div>"
    return html + "</body>"

@app.get("/set/{uid}/{action}")
async def set_status(uid: str, action: str):
    conn = sqlite3.connect('users.db')
    if action == "2": conn.execute('UPDATE users SET status=2 WHERE uid=?', (uid,))
    elif action == "3": conn.execute('UPDATE users SET status=3, key=? WHERE uid=?', (str(uuid.uuid4())[:8], uid))
    elif action == "cancel": conn.execute('DELETE FROM users WHERE uid=?', (uid,))
    conn.commit()
    return "<h1>ОК</h1><a href='/admin'>Назад</a>"
