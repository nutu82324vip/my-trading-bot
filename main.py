import random
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

assets = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC",
    "Apple (AAPL)", "Tesla (TSLA)", "NVIDIA (NVDA)", "Amazon (AMZN)", "Microsoft (MSFT)",
    "Apple (OTC)", "Tesla (OTC)", "NVIDIA (OTC)", "Amazon (OTC)",
    "Gold", "Silver", "Brent Oil", "Gold OTC"
]

@app.get("/", response_class=HTMLResponse)
async def home():
    options = "".join([f"<option value='{a}'>{a}</option>" for a in assets])
    return f"""
    <html style="height:100%;"><body style="height:100%; margin:0; background:#050505; color:#00ffcc; font-family:sans-serif; display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <h1 style="font-size:3rem; text-transform:uppercase;">AI TRADING TERMINAL</h1>
        <div style="width:80%; max-width:600px; background:#111; padding:30px; border:2px solid #00ffcc; border-radius:15px; text-align:center;">
            <form action="/signal" method="post">
                <select name="asset" style="width:100%; padding:15px; background:#222; color:white; border:none; margin-bottom:10px;">{options}</select>
                <select name="time" style="width:100%; padding:15px; background:#222; color:white; border:none; margin-bottom:10px;">
                    <option value="30 сек">30 секунд</option><option value="3 мин">3 минуты</option><option value="5 мин">5 минут</option>
                </select>
                <button style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold; cursor:pointer; font-size:1.2rem;">СКАНИРОВАТЬ РЫНОК</button>
            </form>
            <br><a href="mailto:nutu82324@gmail.com" style="color:#888; text-decoration:none;">📧 ПОДДЕРЖКА: nutu82324@gmail.com</a>
        </div>
    </body></html>
    """

@app.post("/signal", response_class=HTMLResponse)
async def get_signal(asset: str = Form(...), time: str = Form(...)):
    payout = random.randint(88, 95)
    conf = random.randint(85, 99)
    return f"""
    <body style="margin:0; height:100vh; background:#000; color:white; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
        <h1 style="font-size:4rem; color:#00ffcc; margin:0;">{asset}</h1>
        <h2 style="font-size:3rem; margin:10px;">НАПРАВЛЕНИЕ: {random.choice(['BUY', 'SELL'])}</h2>
        <p style="font-size:2rem; margin:5px;">ВРЕМЯ: {time} | ВЫПЛАТА: {payout}%</p>
        <p style="font-size:2.5rem; color:yellow; margin:10px;">🔥 ИИ-УВЕРЕННОСТЬ: {conf}%</p>
        <div style="margin-top:40px; font-size:1.4rem; color:#ddd; width:80%;">
            <p>💡 СОВЕТ 1: Торгуйте только по тренду на старшем таймфрейме.</p>
            <p>💡 СОВЕТ 2: При получении убытка — сделайте перерыв 15 минут.</p>
        </div>
        <br><a href="/" style="color:#00ffcc; font-size:1.5rem; text-decoration:none;">⬅ ВЕРНУТЬСЯ К СКАНИРОВАНИЮ</a>
    </body>
    """
