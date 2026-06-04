from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
import openai
import base64

app = FastAPI()
# ВСТАВЬ СВОЙ КЛЮЧ СЮДА
openai.api_key = ""import os
from dotenv import load_dotenv # Установи библиотеку: pip install python-dotenv

load_dotenv() # Загружает ключ из файла .env
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 

DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.post("/analyze")
async def analyze_graph(request: Request):
    data = await request.json()
    image_b64 = data['image']
    tf = data['tf']
    exp = data['exp']
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": f"Проанализируй график (ТФ: {tf}, Эксп: {exp}). Дай прогноз ВВЕРХ или ВНИЗ и короткое обоснование."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
        ]}]
    )
    return {"analysis": response.choices[0].message.content}

@app.get("/", response_class=HTMLResponse)
async def index():
    data_json = json.dumps(DATA)
    times = ["1 мин", "5 мин", "15 мин", "30 мин", "1 час"]
    exp_times = ["5 сек", "15 сек", "30 сек", "1 мин", "5 мин", "10 мин"]
    options = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    options_exp = "".join([f"<option value='{t}'>{t}</option>" for t in exp_times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#0a0a0c; color:#fff; font-family:sans-serif; margin:0; padding:10px;">
        <div style="max-width:500px; margin:auto; background:#16161a; padding:20px; border-radius:20px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.5rem;">QUANTUM CORE v4.2</h1>
            <button onclick="openScanner()" style="width:100%; padding:15px; background:#222; border:1px solid #00ffcc; color:#00ffcc; font-weight:bold; border-radius:10px;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; margin-top:10px; background:#1f1f24; color:#fff; border-radius:10px;">
                <option value="Валюты">Валюты</option><option value="Криптовалюты">Криптовалюты</option><option value="Акции">Акции</option>
            </select>
            <select id="asset" style="width:100%; padding:10px; margin-top:5px; background:#1f1f24; color:#fff; border-radius:10px;"></select>
        </div>

        <div id="ar-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; background:#000;">
            <video id="video" autoplay playsinline style="width:100%; height:50%; object-fit:cover;"></video>
            <canvas id="canvas" style="display:none;"></canvas>
            <div style="padding:15px; background:rgba(0,0,0,0.95); text-align:center;">
                <div style="display:flex; gap:10px; margin-bottom:10px;">
                    <select id="tf" style="flex:1; padding:10px; background:#222; color:#fff; border-radius:8px;">{options}</select>
                    <select id="exp" style="flex:1; padding:10px; background:#222; color:#fff; border-radius:8px;">{options_exp}</select>
                </div>
                <button onclick="runSmartScan()" style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px;">СКАНИРОВАТЬ ГРАФИК</button>
                <div id="scan-res" style="margin-top:10px; color:#fff; font-size:1.1rem;"></div>
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
            updateAssets();

            function openScanner() {{ document.getElementById('ar-overlay').style.display = 'block'; navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }}).then(s => document.getElementById('video').srcObject = s); }}
            
            async function runSmartScan() {{
                const res = document.getElementById('scan-res');
                res.innerHTML = "🧠 ИИ анализирует...";
                const canvas = document.getElementById('canvas');
                canvas.width = document.getElementById('video').videoWidth;
                canvas.height = document.getElementById('video').videoHeight;
                canvas.getContext('2d').drawImage(document.getElementById('video'), 0, 0);
                const img = canvas.toDataURL('image/jpeg').split(',')[1];
                
                const r = await fetch('/analyze', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{image: img, tf: document.getElementById('tf').value, exp: document.getElementById('exp').value}})
                }});
                const d = await r.json();
                res.innerHTML = d.analysis;
            }}
        </script>
    </body></html>
    """
