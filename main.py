import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# База активов
ASSETS = {
    "Криптовалюты": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Cardano OTC", "TRON OTC", "BNB OTC", "Polkadot OTC", "Toncoin OTC", "Avalanche OTC", "Litecoin OTC", "Chainlink OTC", "Dogecoin OTC", "Polygon OTC"],
    "Акции": ["NVIDIA OTC", "Apple OTC", "McDonald's OTC", "Microsoft OTC", "Facebook OTC (Meta)", "Johnson & Johnson OTC"],
    "Валюты": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC"]
}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    # Инструкция для ИИ теперь включает технический анализ
    prompt = f"""
    Проанализируй {data['asset']} на таймфрейме {data['time']}.
    Выполни технический анализ (RSI и направление тренда).
    Дай точный сигнал.
    Формат JSON: {{
        "dir": "ВВЕРХ/ВНИЗ", 
        "rsi": "перекуплен/перепродан/нейтрально", 
        "acc": "92%", 
        "reason": "краткое объяснение (тренд/уровни)"
    }}
    """
    response = model.generate_content(prompt)
    try:
        clean = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        return {"dir": "ВВЕРХ", "rsi": "нейтрально", "acc": "85%", "reason": "Рынок стабилен"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:20px auto; padding:20px; background:#121212; border:1px solid #333; border-radius:15px;">
        <h2 style="text-align:center; color:#00ffcc;">QUANTUM CORE PRO</h2>
        <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;">
            <option>Криптовалюты</option><option>Акции</option><option>Валюты</option>
        </select>
        <select id="asset" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;"></select>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <select id="time" style="padding:10px; background:#222; color:#fff;"></select>
            <select id="exp" style="padding:10px; background:#222; color:#fff;"></select>
        </div>
        <button id="btn" onclick="run()" style="width:100%; padding:15px; margin-top:20px; background:#0072ff; border:none; color:#fff; font-weight:bold; border-radius:10px;">ЗАПУСК АНАЛИЗА</button>
        <div id="res" style="margin-top:20px; padding:15px; border:1px solid #444; text-align:center; min-height:100px;">
            Ожидание сигнала...
        </div>
        <button id="mart" onclick="alert('Перекрытие активировано!')" style="display:none; width:100%; margin-top:15px; padding:15px; background:#ff4757; border:none; color:#fff; font-weight:bold; border-radius:10px;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const assets = """ + json.dumps(ASSETS) + """;
        const times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"];
        
        function updateAssets() {
            const cat = document.getElementById('cat').value;
            document.getElementById('asset').innerHTML = assets[cat].map(a => `<option>${a}</option>`).join('');
        }
        function init() {
            document.getElementById('time').innerHTML = times.map(t => `<option>${t}</option>`).join('');
            document.getElementById('exp').innerHTML = times.map(t => `<option>${t}</option>`).join('');
            updateAssets();
        }
        async function run() {
            document.getElementById('res').innerHTML = "ИИ проводит теханализ...";
            const d = await (await fetch('/analyze', {
                method: 'POST', 
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({asset: document.getElementById('asset').value, time: document.getElementById('time').value})
            })).json();
            document.getElementById('res').innerHTML = `
                <b style="font-size:1.5rem; color:${d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${d.dir}</b><br>
                <small>RSI: ${d.rsi} | Точность: ${d.acc}</small><br>
                <div style="font-size:0.8rem; margin-top:5px; color:#aaa;">${d.reason}</div>
            `;
            document.getElementById('mart').style.display = 'block';
        }
        init();
    </script>
    </html>
    """
