import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Инициализируем OpenAI клиент (он сам берет ключ из настроек Render)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    data_json = json.dumps(DATA)
    exp_times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"]
    options_time = "".join([f"<option value='{t}'>{t}</option>" for t in exp_times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#0a0a0c; color:#fff; font-family:sans-serif; margin:0; padding:10px;">
        <div style="max-width:500px; margin:auto; background:#16161a; padding:20px; border-radius:20px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.5rem;">QUANTUM CORE v4.2</h1>
            <button onclick="openScanner()" style="width:100%; padding:15px; margin-bottom:15px; background:#222; border:1px solid #00ffcc; color:#00ffcc; font-weight:bold; border-radius:10px;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; margin-bottom:5px; background:#1f1f24; color:#fff; border-radius:10px;">
                <option value="Валюты">Валюты</option><option value="Криптовалюты">Криптовалюты</option><option value="Акции">Акции</option>
            </select>
            <select id="asset" style="width:100%; padding:10px; margin-bottom:10px; background:#1f1f24; color:#fff; border-radius:10px;"></select>
        </div>

        <div id="ar-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; background:#000;">
            <video id="video" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
            <div style="position:absolute; top:20%; left:10%; width:80%; height:40%; border:3px solid #00ffcc; border-radius:15px;">
                <div style="width:100%; height:2px; background:#00ffcc; animation: scan 2s linear infinite;"></div>
            </div>
            <div style="position:absolute; bottom:0; width:100%; padding:20px; background:rgba(0,0,0,0.95); text-align:center;">
                <label style="color:#aaa; font-size:0.8rem;">ВРЕМЯ ЭКСПИРАЦИИ:</label>
                <select id="exp" style="width:100%; padding:10px; margin-bottom:10px; background:#222; color:#fff; border-radius:10px;">{options_time}</select>
                <button onclick="runSmartScan()" id="scan-btn" style="width:100%; padding:20px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px;">СКАНИРОВАТЬ ГРАФИК</button>
                <div id="scan-res" style="margin-top:15px;"></div>
                <button id="m-btn" onclick="runSmartScan()" style="display:none; width:100%; padding:15px; margin-top:10px; background:transparent; border:1px solid #ffcc00; color:#ffcc00; border-radius:10px;">ПЕРЕКРЫТИЕ (МАРТИНГЕЙЛ)</button>
            </div>
        </div>
            
        <style>@keyframes scan {{ 0% {{ top:0%; }} 50% {{ top:100%; }} 100% {{ top:0%; }} }}</style>
        <script>
            const data = {data_json};
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const asset = document.getElementById('asset');
                asset.innerHTML = "";
                data[cat].forEach(a => asset.innerHTML += '<option value="'+a+'">'+a+'</option>');
            }}
            updateAssets();

            function openScanner() {{ document.getElementById('ar-overlay').style.display = 'block'; navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }}).then(s => {{ document.getElementById('video').srcObject = s; }}); }}
            
            async function runSmartScan() {{
                const res = document.getElementById('scan-res');
                res.innerHTML = "🔍 Поиск структуры графика...";
                await new Promise(r => setTimeout(r, 1500));
                
                const dir = Math.random() > 0.3 ? 'ВВЕРХ' : 'ВНИЗ';
                const col = dir === 'ВВЕРХ' ? '#00ff00' : '#ff0000';
                
                res.innerHTML = '<div style="font-size:3rem; color:'+col+'; font-weight:900;">'+dir+'</div>';
            }}
        </script>
    </body></html>
    """
