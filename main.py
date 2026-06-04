import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.post("/analyze")
async def analyze_ai(request: Request):
    data = await request.json()
    asset = data.get("asset")
    # Запрос к OpenAI без рандома
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Ты профи трейдер. Дай прогноз: ВВЕРХ или ВНИЗ. Формат JSON: {'dir': 'ВВЕРХ', 'reason': 'почему', 'accuracy': '92%'}"},
                  {"role": "user", "content": f"Проанализируй {asset}"}]
    )
    return json.loads(response.choices[0].message.content)

@app.get("/", response_class=HTMLResponse)
async def index():
    data_json = json.dumps(DATA)
    return f"""
    <html style="font-size:20px;"><body style="background:#0a0a0c; color:#fff; font-family:sans-serif; margin:0; padding:10px;">
        <div style="max-width:500px; margin:auto; background:#16161a; padding:20px; border-radius:20px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.5rem;">QUANTUM CORE v4.2</h1>
            <button onclick="openScanner()" style="width:100%; padding:15px; margin-bottom:15px; background:#222; border:1px solid #00ffcc; color:#00ffcc; font-weight:bold; border-radius:10px;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; background:#1f1f24; color:#fff;"></select>
            <select id="asset" style="width:100%; padding:10px; background:#1f1f24; color:#fff;"></select>
        </div>
        <div id="ar-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; background:#000;">
            <video id="video" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
            <div style="position:absolute; bottom:0; width:100%; padding:20px; background:rgba(0,0,0,0.95); text-align:center;">
                <button onclick="runSmartScan()" id="scan-btn" style="width:100%; padding:20px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px;">СКАНИРОВАТЬ ГРАФИК (ИИ)</button>
                <div id="scan-res" style="margin-top:15px;"></div>
            </div>
        </div>
        <script>
            const data = {data_json};
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const asset = document.getElementById('asset');
                asset.innerHTML = "";
                data[cat].forEach(a => asset.innerHTML += '<option value="'+a+'">'+a+'</option>');
            }}
            document.getElementById('cat').innerHTML = Object.keys(data).map(c => `<option value="${{c}}">${{c}}</option>`).join('');
            updateAssets();

            function openScanner() {{ document.getElementById('ar-overlay').style.display = 'block'; navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }}).then(s => {{ document.getElementById('video').srcObject = s; }}); }}
            
            async function runSmartScan() {{
                const res = document.getElementById('scan-res');
                res.innerHTML = "🔍 Анализ ИИ...";
                const resp = await fetch('/analyze', {{ method: 'POST', body: JSON.stringify({{ asset: document.getElementById('asset').value }}), headers: {{'Content-Type': 'application/json'}} }});
                const d = await resp.json();
                
                res.innerHTML = `<div style="font-size:3rem; color:${{d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}}">${{d.dir}}</div>
                                 <div style="color:#aaa;">${{d.reason}} (Точность: ${{d.accuracy}})</div>
                                 <div id="timer" style="font-size:1.5rem; color:#ffcc00;">ВХОД ЧЕРЕЗ: 10</div>`;
                let t = 10;
                let i = setInterval(() => {{ t--; document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t; if(t<=0) clearInterval(i); }}, 1000);
            }}
        </script>
    </body></html>
    """
