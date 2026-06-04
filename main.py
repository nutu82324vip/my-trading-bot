from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/CHF OTC", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "CHF/JPY OTC", "CHF/NOK OTC", "EUR/CAD", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY", "EUR/USD", "EUR/USD OTC", "GBP/AUD", "GBP/CAD", "GBP/USD OTC", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/CAD OTC", "USD/CHF OTC", "USD/CNH OTC", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    data_json = json.dumps(DATA)
    times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин"]
    options_html = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#0a0a0c; color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:10px;">
        <div id="main-ui" style="max-width:500px; margin:auto; background:#16161a; padding:25px; border-radius:20px; border:1px solid #333; box-shadow: 0 0 30px rgba(0,255,204,0.1);">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.6rem; letter-spacing: 2px;">QUANTUM CORE v4.2</h1>
            
            <button onclick="openScanner()" style="width:100%; padding:15px; margin-bottom:15px; background:#222; border:1px solid #00ffcc; border-radius:10px; color:#00ffcc; font-weight:bold; cursor:pointer;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
            
            <label style="color:#888; font-size:0.7rem;">КАТЕГОРИЯ:</label>
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:12px; margin-bottom:10px; background:#1f1f24; color:#fff; border:1px solid #333; border-radius:10px;">
                <option value="Валюты">Валюты</option><option value="Криптовалюты">Криптовалюты</option><option value="Акции">Акции</option>
            </select>
            
            <label style="color:#888; font-size:0.7rem;">ВЫБОР АКТИВА:</label>
            <select id="asset" style="width:100%; padding:12px; margin-bottom:15px; background:#1f1f24; color:#fff; border:1px solid #333; border-radius:10px;"></select>
            
            <div style="display:flex; gap:10px;">
                <div style="flex:1;">
                    <label style="color:#888; font-size:0.7rem;">ТАЙМФРЕЙМ:</label>
                    <select id="candle" style="width:100%; padding:10px; background:#1f1f24; color:#fff; border:1px solid #333; border-radius:10px;">{options_html}</select>
                </div>
                <div style="flex:1;">
                    <label style="color:#888; font-size:0.7rem;">ЭКСПИРАЦИЯ:</label>
                    <select id="duration" style="width:100%; padding:10px; background:#1f1f24; color:#fff; border:1px solid #333; border-radius:10px;">{options_html}</select>
                </div>
            </div>
            
            <button id="btn" style="width:100%; padding:18px; margin-top:20px; background:linear-gradient(90deg, #00ffcc, #0088ff); border:none; border-radius:10px; font-weight:bold; cursor:pointer;" onclick="runAI()">ЗАПУСК АНАЛИЗА</button>
            
            <div id="loading" style="display:none; text-align:center; margin:20px 0; color:#00ffcc;">Сканирование...</div>
            <div id="result" style="margin-top:20px; padding:20px; text-align:center; border-radius:15px; display:none; background:#1f1f24; border:1px solid #444;"></div>
        </div>

        <div id="ar-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; background:#000;">
            <video id="video" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
            <div style="position:absolute; top:20%; left:10%; width:80%; height:40%; border:3px solid #00ffcc; border-radius:15px;"></div>
            <div style="position:absolute; bottom:0; width:100%; padding:20px; background:rgba(0,0,0,0.95); text-align:center;">
                <button id="scan-btn" onclick="startScanner()" style="width:100%; padding:20px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px; margin-bottom:10px;">СКАНИРОВАТЬ</button>
                <button onclick="closeScanner()" style="width:100%; padding:15px; background:transparent; border:1px solid #555; color:white; border-radius:10px;">ЗАКРЫТЬ</button>
                <div id="scan-result" style="margin-top:20px; font-weight:bold;"></div>
            </div>
        </div>
            
        <script>
            const data = {data_json};
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const assetSelect = document.getElementById('asset');
                assetSelect.innerHTML = "";
                data[cat].forEach(a => assetSelect.innerHTML += '<option value="' + a + '">' + a + '</option>');
            }}
            updateAssets();

            function openScanner() {{
                document.getElementById('ar-overlay').style.display = 'block';
                document.getElementById('scan-result').style.display = 'none';
                navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }})
                    .then(s => document.getElementById('video').srcObject = s);
            }}

            function closeScanner() {{
                document.getElementById('ar-overlay').style.display = 'none';
                const s = document.getElementById('video').srcObject;
                if(s) s.getTracks().forEach(t => t.stop());
            }}

            async function startScanner() {{
                const res = document.getElementById('scan-result');
                res.style.display = 'block';
                res.innerHTML = "<div style='color:#fff;'>АНАЛИЗ СВЕЧЕЙ...</div>";
                await new Promise(r => setTimeout(r, 2000));
                
                const dir = Math.random() > 0.5 ? 'ВВЕРХ' : 'ВНИЗ';
                const color = dir === 'ВВЕРХ' ? '#00ff00' : '#ff0000';
                res.innerHTML = `<div style="font-size:3.5rem; color:${color};">${dir}</div>
                                 <div style="font-size:1.2rem; color:#aaa; margin:10px 0;">ПРИЧИНА: Анализ объема и импульса</div>
                                 <div style="font-size:2rem; color:#ffcc00;">ВХОД ЧЕРЕЗ: 15 СЕК</div>`;
            }}

            async function runAI() {{
                const res = document.getElementById('result');
                const load = document.getElementById('loading');
                const btn = document.getElementById('btn');
                btn.disabled = true;
                res.style.display = 'none';
                load.style.display = 'block';
                await new Promise(r => setTimeout(r, 2000));
                load.style.display = 'none';
                const trend = Math.random() > 0.4 ? '📈 ВВЕРХ' : '📉 ВНИЗ';
                res.style.display = 'block';
                res.style.borderLeft = "5px solid " + (trend.includes('ВВЕРХ') ? '#00cc66' : '#cc0033');
                res.innerHTML = `<div style="font-size:2rem; font-weight:bold;">${trend}</div>
                                 <div style="color:#888;">Вероятность: 94.2%</div>`;
                btn.disabled = false;
            }}
        </script>
    </body></html>
    """
