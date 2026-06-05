import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# База из 70+ активов
ASSETS = {
    "Криптовалюты": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Cardano OTC", "TRON OTC", "BNB OTC", "Polkadot OTC", "Toncoin OTC", "Avalanche OTC", "Litecoin OTC", "Chainlink OTC", "Dogecoin OTC", "Polygon OTC", "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD", "DOGE/USD", "MATIC/USD"],
    "Валюты": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC", "AUD/JPY OTC", "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD", "EUR/GBP", "GBP/JPY"],
    "Акции": ["NVIDIA OTC", "Apple OTC", "McDonald's OTC", "Microsoft OTC", "Facebook OTC", "Tesla OTC", "Amazon OTC", "Google OTC", "Netflix OTC", "Coca-Cola OTC", "PepsiCo OTC", "Intel OTC", "AMD OTC", "PayPal OTC", "Disney OTC", "Boeing OTC", "Visa OTC", "Mastercard OTC", "NVIDIA", "Apple", "Tesla", "Amazon"]
}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    prompt = f"Торговый сигнал для актива {data['asset']}. Напиши только: ВВЕРХ или ВНИЗ. И точность %. Например: ВВЕРХ | 92%"
    response = model.generate_content(prompt)
    return {"result": response.text.strip()}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:20px auto; padding:20px; background:#121212; border:1px solid #333; border-radius:15px;">
        <h2 style="text-align:center; color:#00ffcc;">QUANTUM CORE v4.2</h2>
        <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;">
            <option>Криптовалюты</option><option>Валюты</option><option>Акции</option>
        </select>
        <select id="asset" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;"></select>
        <select id="time" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:20px;">
            <option>5 сек</option><option>15 сек</option><option>30 сек</option><option>1 мин</option><option>5 мин</option><option>10 мин</option>
        </select>
        <button id="btn" onclick="run()" style="width:100%; padding:20px; background:#0072ff; border:none; color:#fff; font-weight:bold; border-radius:10px;">ЗАПУСК АНАЛИЗА</button>
        <div id="res" style="margin-top:20px; padding:15px; border:1px solid #444; text-align:center; font-size:24px; color:#fff;">Ожидание...</div>
        <button id="mart" onclick="alert('Перекрытие!')" style="display:none; width:100%; margin-top:15px; padding:15px; background:#ff4757; border:none; color:#fff; font-weight:bold; border-radius:10px;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const assets = """ + json.dumps(ASSETS) + """;
        function updateAssets() {
            const cat = document.getElementById('cat').value;
            document.getElementById('asset').innerHTML = assets[cat].map(a => `<option>${a}</option>`).join('');
        }
        async function run() {
            const res = document.getElementById('res');
            res.innerHTML = "Анализирую...";
            try {
                const r = await fetch('/analyze', {
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({asset: document.getElementById('asset').value, time: document.getElementById('time').value})
                });
                const d = await r.json();
                res.innerHTML = d.result;
                document.getElementById('mart').style.display = 'block';
            } catch(e) { res.innerHTML = "Ошибка связи."; }
        }
        updateAssets();
    </script>
    </html>
    """
