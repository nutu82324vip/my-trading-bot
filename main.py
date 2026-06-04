from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "EUR/USD", "GBP/AUD", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    data_json = json.dumps(DATA)
    times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"]
    options = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
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
            <video id="video" autoplay playsinline style="width:100%; height:60%; object-fit:cover;"></video>
            <canvas id="canvas" style="display:none;"></canvas>
            
            <div style="padding:15px; background:rgba(0,0,0,0.95); text-align:center;">
                <div style="display:flex; gap:10px; margin-bottom:10px;">
                    <select id="int" style="flex:1; padding:10px; background:#222; color:#fff; border-radius:8px;">{options}</select>
                    <select id="exp" style="flex:1; padding:10px; background:#222; color:#fff; border-radius:8px;">{options}</select>
                </div>
                <button onclick="runSmartScan()" id="scan-btn" style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold; border-radius:10px;">СКАНИРОВАТЬ ГРАФИК</button>
                <div id="scan-res" style="margin-top:10px; min-height:80px;"></div>
                <button id="m-btn" onclick="runSmartScan()" style="display:none; width:100%; padding:15px; margin-top:5px; background:transparent; border:1px solid #ffcc00; color:#ffcc00; border-radius:10px;">ПЕРЕКРЫТИЕ</button>
            </div>
        </div>
            
        <script>
            const data = {data_json};
            const video = document.getElementById('video');
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const asset = document.getElementById('asset');
                asset.innerHTML = "";
                data[cat].forEach(a => asset.innerHTML += '<option value="'+a+'">'+a+'</option>');
            }}
            updateAssets();

            function openScanner() {{ 
                document.getElementById('ar-overlay').style.display = 'block'; 
                navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }}).then(s => video.srcObject = s); 
            }}
            
            async function runSmartScan() {{
                const res = document.getElementById('scan-res');
                res.innerHTML = "🔍 Анализ свечей...";
                
                // Обработка пикселей через Canvas
                const canvas = document.getElementById('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                const frame = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
                
                let green = 0, red = 0;
                for(let i=0; i < frame.length; i+=4) {{
                    if(frame[i+1] > 150 && frame[i] < 100) green++;
                    if(frame[i] > 150 && frame[i+1] < 100) red++;
                }}
                
                // Проверка: видит ли бот график
                if(green < 1000 && red < 1000) {{
                    res.innerHTML = '<div style="color:red; font-weight:bold;">⚠️ ГРАФИК НЕ ОБНАРУЖЕН!</div>';
                    return;
                }}
                
                const dir = green > red ? "ВВЕРХ" : "ВНИЗ";
                const col = dir === "ВВЕРХ" ? "#00ff00" : "#ff0000";
                
                res.innerHTML = `<div style="font-size:3rem; color:${{col}}; font-weight:900;">${{dir}}</div>
                                 <div style="font-size:1rem;">Интервал: ${{document.getElementById('int').value}} | Эксп: ${{document.getElementById('exp').value}}</div>
                                 <div id="timer" style="font-size:1.5rem; color:#ffcc00; font-weight:bold;">ВХОД ЧЕРЕЗ: 10 СЕК</div>`;
                
                let t = 10;
                let interval = setInterval(() => {{
                    t--;
                    document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t + " СЕК";
                    if (t <= 0) {{ clearInterval(interval); document.getElementById('timer').innerText = "ВХОДИТЕ СЕЙЧАС!"; document.getElementById('m-btn').style.display = 'block'; }}
                }}, 1000);
            }}
        </script>
    </body></html>
    """
