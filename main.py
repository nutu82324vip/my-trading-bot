from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "NZD/USD", "AUD/JPY", "CHF/JPY",
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC", "EUR/JPY OTC", "GBP/JPY OTC", "NZD/USD OTC",
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "LTC/USDT", "ADA/USDT", "DOT/USDT",
    "BTC/USDT OTC", "ETH/USDT OTC", "SOL/USDT OTC", "XRP/USDT OTC", "DOGE/USDT OTC",
    "Apple", "Tesla", "NVIDIA", "Amazon", "Microsoft", "Google", "Netflix", "Meta",
    "Apple OTC", "Tesla OTC", "NVIDIA OTC", "Amazon OTC", "Gold", "Silver", "Brent Oil"
]

@app.get("/", response_class=HTMLResponse)
async def index():
    assets_html = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
    times = "".join([f"<option value='{t}'>{t}</option>" for t in ["5 сек", "30 сек", "1 мин", "3 мин", "5 мин"]])
    
    return f"""
    <html style="font-size:20px;">
    <body style="background:#050505; color:#fff; font-family:sans-serif; margin:0; padding:20px;">
        <div style="max-width:500px; margin:auto; background:#111; padding:30px; border-radius:25px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc;">QUANTUM SCANNER</h1>
            
            <label style="display:block; margin:15px 0 5px;">Актив:</label>
            <select id="asset" style="width:100%; padding:15px; background:#222; color:#fff; border-radius:10px;">{assets_html}</select>
            
            <label style="display:block; margin:15px 0 5px;">Время сделки:</label>
            <select id="time" style="width:100%; padding:15px; background:#222; color:#fff; border-radius:10px;">{times}</select>
            
            <button style="width:100%; padding:20px; margin-top:30px; background:#00ffcc; border:none; border-radius:15px; font-weight:bold; font-size:1.2rem; cursor:pointer;" 
            onclick="generateSignal()">ЗАПУСТИТЬ ИИ АНАЛИЗ</button>
            
            <div id="result" style="margin-top:20px; padding:20px; text-align:center; font-size:1.5rem; font-weight:bold; border-radius:15px; display:none;"></div>
            
            <script>
            function generateSignal() {{
                const res = document.getElementById('result');
                const asset = document.getElementById('asset').value;
                const signals = ['📈 ВВЕРХ (CALL)', '📉 ВНИЗ (PUT)'];
                const randomSignal = signals[Math.floor(Math.random() * signals.length)];
                
                res.style.display = 'block';
                res.style.background = randomSignal.includes('ВВЕРХ') ? '#00cc66' : '#cc0033';
                res.innerHTML = asset + ': ' + randomSignal;
            }}
            </script>
        </div>
    </body>
    </html>
    """
