import random
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Полный список активов
assets = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC",
    "Apple (AAPL)", "Tesla (TSLA)", "NVIDIA (NVDA)", "Amazon (AMZN)", "Microsoft (MSFT)",
    "Apple (OTC)", "Tesla (OTC)", "NVIDIA (OTC)", "Amazon (OTC)",
    "Gold", "Silver", "Brent Oil", "Gold OTC"
]

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, status TEXT)')
    conn.commit()
    conn.close()

init_db()

# Функция генерации сигнала с ИИ-стилем
def get_signal_ui():
    asset = random.choice(assets)
    direction = random.choice(['📈 🟢 BUY', '📉 🔴 SELL'])
    confidence = random.randint(80, 99)
    payout = random.randint(88, 95)
    
    return f"""
    <div style="background:#2d3748; padding:20px; border-radius:10px; border:1px solid #4a5568; display:inline-block;">
        <h2 style="color:#63b3ed;">📡 AI SIGNAL</h2>
        <p>🔹 <b>Активы:</b> {asset}</p>
        <p>⚡️ <b>Направление:</b> {direction}</p>
        <p>📊 <b>ТФ:</b> M3 | ⏱ <b>Время:</b> 3 мин</p>
        <p>🎯 <b>Выплата:</b> {payout}%</p>
        <p style="color:#68d391; font-size:1.2em;">🔥 <b>Уверенность:</b> {confidence}%</p>
    </div>
    """

@app.get("/", response_class=HTMLResponse)
async def home():
    return """<body style="background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding-top:50px;">
    <h1>⚡️ AI SCANNER PRO</h1>
    <form action="/login" method="post">
        <input name="uid" placeholder="Ваш ID" style="padding:10px; width:250px; border-radius:5px;"><br><br>
        <button style="padding:10px 30px; background:#3182ce; color:white; border:none; border-radius:5px; cursor:pointer;">ВОЙТИ</button>
    </form></body>"""

@app.post("/login")
async def login(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT status FROM users WHERE uid=?', (uid,)).fetchone()
    if not user:
        conn.execute('INSERT INTO users VALUES (?, ?)', (uid, 'pending'))
        conn.commit()
        return "<body style='background:#0f172a; color:white; text-align:center;'><h1>Заявка принята. Ожидайте активации.</h1></body>"
    
    if user[0] == 'active':
        return f"<body style='background:#0f172a; color:white; text-align:center; padding-top:50px;'>{get_signal_ui()}<br><br><button onclick='location.reload()' style='padding:10px 20px;'>🔄 ЕЩЕ СИГНАЛ</button></body>"
    
    return "<body style='background:#0f172a; color:white; text-align:center;'><h1>Ожидайте активации администратором.</h1></body>"

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    html = "<body style='background:#1a202c; color:white; padding:20px;'><h1>Панель администратора:</h1>"
    for u in users:
        html += f"<p>ID: {u[0]} | Статус: {u[1]} | <a href='/approve/{u[0]}' style='color:#63b3ed;'>[ОДОБРИТЬ]</a></p>"
    return html + "</body>"

@app.get("/approve/{uid}")
async def approve(uid: str):
    conn = sqlite3.connect('users.db')
    conn.execute('UPDATE users SET status=? WHERE uid=?', ('active', uid))
    conn.commit()
    return "<h1>Успешно! <a href='/admin'>Вернуться</a></h1>"
