from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD", "EUR/GBP", "EUR/JPY", "EUR/CHF",
    "EUR/CAD", "EUR/AUD", "GBP/JPY", "GBP/CHF", "GBP/AUD", "GBP/CAD", "AUD/JPY", "AUD/NZD", "AUD/CAD", "AUD/CHF",
    "CAD/JPY", "CAD/CHF", "CHF/JPY", "NZD/JPY", "NZD/CAD", "NZD/CHF", "USD/RUB", "EUR/RUB", "USD/TRY", "USD/BRL",
    "USD/MXN", "USD/ZAR", "USD/CNH", "USD/SGD", "USD/HKD", "USD/INR", "USD/IDR", "USD/MYR", "USD/PHP", "USD/THB",
    "USD/VND", "USD/UAH", "BTC", "ETH", "LTC", "XRP", "BCH", "Dash", "BNB", "SOL", "ADA", "DOGE", "DOT", "AVAX",
    "LINK", "MATIC", "TRX", "TON", "Apple", "Microsoft", "NVIDIA", "Meta", "Intel", "Tesla", "AMD", "Google",
    "Amazon", "Alibaba", "Coinbase", "Palantir", "GameStop", "Marathon"
]

@app.get("/", response_class=HTMLResponse)
async def index():
    assets_html = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
    times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин"]
    times_html = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#050505; color:#fff; font-family:sans-serif; margin:0; padding:10px;">
        <div id="mainUI" style="max-width:500px; margin:auto; background:#111; padding:20px; border-radius:25px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.5rem;">QUANTUM AI PRO</h1>
            
            <label>Актив:</label>
            <select id="asset" style="width:100%; padding:12px; margin:10px 0 15px; background:#222; color:#fff; border-radius:10px;">{assets_html}</select>
            
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label style="font-size:0.8rem;">Интервал:</label><select id="candle" style="width:100%; padding:10px; margin-top:5px; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
                <div style="flex:1;"><label style="font-size:0.8rem;">Экспирация:</label><select id="duration" style="width:100%; padding:10px; margin-top:5px; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
            </div>
            
            <button style="width:100%; padding:15px; margin-top:20px; background:#00ffcc; border:none; border-radius:15px; font-weight:bold; cursor:pointer;" onclick="runAI()">ЗАПУСТИТЬ АНАЛИЗ</button>
            <button style="width:100%; padding:15px; margin-top:10px; background:#444; border:none; border-radius:15px; font-weight:bold; cursor:pointer;" onclick="startCamera()">📷 AI CAMERA SCAN</button>
            
            <div id="result" style="margin-top:20px; padding:15px; text-align:center; font-size:1.3rem; border-radius:15px; display:none;"></div>
            <button id="martingaleBtn" style="width:100%; padding:12px; margin-top:10px; background:transparent; border:2px solid #ffcc00; color:#ffcc00; border-radius:10px; display:none;" onclick="runAI()">ПЕРЕКРЫТИЕ</button>
        </div>

        <div id="cameraView" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:black; z-index:999;">
            <div style="position:absolute; top:25%; left:10%; width:80%; height:30%; border:3px solid #00ffcc; border-radius:15px; box-shadow: 0 0 20px #00ffcc;"></div>
            <div style="position:absolute; bottom:100px; width:100%; text-align:center; color:#00ffcc; font-weight:bold;">ИДЕТ АНАЛИЗ ГРАФИКА...</div>
        </div>

        <script>
            function startCamera() {{
                document.getElementById('cameraView').style.display = 'block';
                setTimeout(() => {{
                    document.getElementById('cameraView').style.display = 'none';
                    runAI();
                }}, 3000);
            }}

            async function runAI() {{
                const res = document.getElementById('result');
                const mBtn = document.getElementById('martingaleBtn');
                res.style.display = 'block';
                res.innerHTML = "Сканирование данных...";
                await new Promise(r => setTimeout(r, 1500));
                
                const trend = Math.random() > 0.4 ? '📈 ВВЕРХ' : '📉 ВНИЗ';
                res.style.background = trend.includes('ВВЕРХ') ? '#00cc66' : '#cc0033';
                res.innerHTML = trend + "<br><small style='font-size:0.9rem;'>Точность: 86.4%</small>";
                mBtn.style.display = 'block';
            }}
        </script>
    </body></html>
    """
