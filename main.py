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

# Функция красивого оформления страницы
def layout(content):
    return f"""<html style="font-size:20px;"><body style="background:#050505; color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:20px;">
        <div style="max-width:600px; margin:auto; background:#111; padding:40px; border-radius:30px; border:1px solid #333; box-shadow:0 0 50px rgba(0,255,204,0.1);">
            {content}
        </div>
    </body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index(uid: str = Cookie(None)):
    if not uid:
        return layout('<h1 style="color:#00ffcc;">QUANTUM ACCESS</h1><form action="/login" method="post"><input name="uid" placeholder="Введите ваш ID" style="width:100%; padding:20px; font-size:1.5rem; background:#222; color:white; border:none; border-radius:15px; margin-bottom:20px;"><button style="width:100%; padding:20px; font-size:1.5rem; background:#fff; border:none; border-radius:15px; cursor:pointer;">ВОЙТИ</button></form>')
    
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT status FROM users WHERE uid=?', (uid,)).fetchone()
    
    if user and user[0] == 3: # Активен
        opts = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
        times = "".join([f"<option value='{t}'>{t}</option>" for t in ["5 сек", "30 сек", "1 мин", "5 мин"]])
        return layout(f"""<h1 style="color:#00ffcc;">QUANTUM SCANNER</h1>
            <label>Выберите актив:</label><select style="width:100%; padding:15px; margin-bottom:20px; background:#222; color:white;">{opts}</select>
            <label>Таймфрейм свечи:</label><select style="width:100%; padding:15px; margin-bottom:20px; background:#222; color:white;">{times}</select>
            <label>Длительность сделки:</label><select style="width:100%; padding:15px; margin-bottom:20px; background:#222; color:white;">{times}</select>
            <button style="width:100%; padding:20px; background:#00ffcc; border:none; border-radius:15px; font-weight:bold;">ЗАПУСТИТЬ АНАЛИЗ</button>
            <p style="margin-top:20px; color:#888;">Поддержка: t.me/ваш_тг</p>""")
    
    return layout('<h1 style="color:#ffcc00;">СТАТУС: ОЖИДАНИЕ</h1><p>Система проверяет вашу оплату. Ожидайте активации администратором.</p>')

@app.post("/login")
async def login(uid: str = Form(...)):
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
    html = "<body style='background:#000; color:#fff; padding:40px;'>"
    for u in users:
        html += f"<div style='border:1px solid #444; padding:20px; margin-bottom:10px;'>ID: {u[0]} | Статус: {u[2]} | <a href='/set/{u[0]}/3' style='color:#0ff;'>[АКТИВИРОВАТЬ]</a></div>"
    return html + "</body>"

@app.get("/set/{uid}/{status}")
async def set_status(uid: str, status: int):
    conn = sqlite3.connect('users.db')
    conn.execute('UPDATE users SET status=? WHERE uid=?', (status, uid))
    conn.commit()
    return "<h1>Готово!</h1>"
