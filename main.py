import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 70+ активов: ВСЁ ВКЛЮЧЕНО
ASSETS = {
    "Криптовалюты": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Cardano OTC", "TRON OTC", "BNB OTC", "Polkadot OTC", "Toncoin OTC", "Avalanche OTC", "Litecoin OTC", "Chainlink OTC", "Dogecoin OTC", "Polygon OTC", "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD", "DOT/USD", "DOGE/USD"],
    "Валюты": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC", "AUD/JPY OTC", "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD", "EUR/GBP", "GBP/JPY", "AUD/CAD", "EUR/AUD", "CAD/JPY", "CHF/JPY"],
    "Акции": ["NVIDIA OTC", "Apple OTC", "McDonald's OTC", "Microsoft OTC", "Facebook OTC", "Tesla OTC", "Amazon OTC", "Google OTC", "Netflix OTC", "Coca-Cola OTC", "PepsiCo OTC", "Intel OTC", "AMD OTC", "PayPal OTC", "Disney OTC", "Boeing OTC", "Visa OTC", "Mastercard OTC", "NVIDIA", "Apple", "Tesla", "Amazon", "GOOGL", "META", "MSFT"]
}

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        prompt = f"Сигнал для {data['asset']} ({data['time']}). Пиши только: ВВЕРХ или ВНИЗ и %. Пример: ВВЕРХ | 90%"
        response = model.generate_content(prompt)
        return {"result": response.text.strip()}
    except:
        return {"result": "Попробуй еще раз"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:20px auto; padding:20px; background:#121212; border:1px solid #333; border-radius:15px;">
        <h2 style="text-align:center; color:#00ffcc;">QUANTUM CORE v4.2</h2>
        <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;"></select>
        <select id="asset" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;"></select>
        <button id="btn" onclick="run()" style="width:100%; padding:20px; background:#0072ff; border:none; color:#fff; font-weight:bold; border-radius:10px;">ЗАПУСК АНАЛИЗА</button>
        <div id="res" style="margin-top:20px; padding:15px; border:1px solid #444; text-align:center; font-size:22px;">Готов к работе</div>
        <button id="mart" onclick="alert('Перекрытие!')" style="display:none; width:100%; margin-top:15px; padding:15px; background:#ff4757; border:none; color:#fff; font-weight:bold; border-radius:10px;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const assets = """ + json.dumps(ASSETS) + """;
        const catS = document.getElementById('cat');
        Object.keys(assets).forEach(c => catS.innerHTML += `<option>${c}</option>`);
        function updateAssets() {
            document.getElementById('asset').innerHTML = assets[catS.value].map(a => `<option>${a}</option>`).join('');
        }
        async function run() {
            const res = document.getElementById('res');
            res.innerHTML = "Анализирую...";
            const r = await fetch('/analyze', {method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({asset: document.getElementById('asset').value, time: '1 мин'})
            });
            const d = await r.json();
            res.innerHTML = d.result;
            document.getElementById('mart').style.display = 'block';
        }
        updateAssets();
    </script>
    </html>
    """
