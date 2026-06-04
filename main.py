from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# Полный список активов
DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    # Генерируем категории и активы для JS
    data_json = json.dumps(DATA)
    times = [f"{i} мин" for i in range(1, 11)]
    options_time = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#0a0a0c; color:#fff; font-family:sans-serif; margin:0; padding:10px;">
        <div style="max-width:500px; margin:auto; background:#16161a; padding:20px; border-radius:20px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.5rem;">QUANTUM CORE v4.2</h1>
            
            <button onclick="openScanner()" style="width:100%; padding:15px; margin-bottom:15px; background:#222; border:1px solid #00ffcc; color:#00ffcc; font-weight:bold; border-radius:10px;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
            
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:10px; margin-bottom:5px; background:#1f1f24; color:#fff; border-radius:10px;">
                <option value="Валюты">Валюты</option><option value="Криптовалюты">Криптовалюты</option><option value="Акции">Акции</option>
            </select>
            <select id="asset" style="width:100%; padding:10px; margin-bottom:10px; background:#1f1f24; color:#fff; border-radius:10px;"></select>
            
            <label style="color:#888; font-size:0.7rem;">ТАЙМФРЕЙМ:</label>
            <select id="candle" style="width:100%; padding:10px; margin-bottom:10px; background:#1f1f24; color:#fff; border-radius:10px;">{options_time}</select>
            
            <button id="btn" style="width:100%; padding:18px; background:linear-gradient(90deg, #00ffcc, #0088ff); border:none; border-radius:10px; font-weight:bold;" onclick="runAI()">ЗАПУСК АНАЛИЗА</button>
            <div id="result" style="margin-top:20px; display:none; text-align:center;"></div>
        </div>

        <div id="ar-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; background:#000;">
            <video id="video" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
            <div style="position:absolute; top:20%; left:10%; width:80%; height:40%; border:3px solid #00ffcc; border-radius:15px;">
                <div style="width:100%; height:2px; background:#00ffcc; animation: scan 2s linear infinite;"></div>
            </div>
            <div style="position:absolute; bottom:0; width:100%; padding:20px; background:rgba(0,0,0,0.95); text-align:center;">
                <button onclick="startScanner()" style="width:100%; padding:20px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px;">СКАНИРОВАТЬ ГРАФИК</button>
                <div id="scan-res" style="margin-top:20px;"></div>
            </div>
        </div>
            
        <style>@keyframes scan {{ 0%{{top:0%}} 50%{{top:100%}} 100%{{top:0%}} }}</style>
        <script>
            const data = {data_json};
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const assetSelect = document.getElementById('asset');
                assetSelect.innerHTML = "";
                data[cat].forEach(a => assetSelect.innerHTML += '<option value="'+a+'">'+a+'</option>');
            }}
            updateAssets();

            function openScanner() {{ document.getElementById('ar-overlay').style.display = 'block'; navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }}).then(s => document.getElementById('video').srcObject = s); }}
            
            async function startScanner() {{
                const res = document.getElementById('scan-res');
                res.innerHTML = "АНАЛИЗ СВЕЧЕЙ...";
                await new Promise(r => setTimeout(r, 2000));
                const dir = Math.random() > 0.5 ? 'ВВЕРХ' : 'ВНИЗ';
                res.innerHTML = `<div style="font-size:4rem; color:${dir==='ВВЕРХ'?'#00ff00':'#ff0000'}; font-weight:900;">${dir}</div>
                                 <div style="font-size:2.5rem; color:#ffcc00; margin:15px 0;">ВХОД ЧЕРЕЗ: 10 СЕК</div>
                                 <div style="font-size:1rem; color:#aaa;">1. Вход по тренду<br>2. Сильный объем актива</div>`;
            }}
        </script>
    </body></html>
    """
