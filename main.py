import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

ASSETS = {
    "Валюты OTC": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC", "AUD/JPY OTC", "CHF/JPY OTC", "EUR/CAD OTC"],
    "Крипта OTC": ["Bitcoin OTC", "Ethereum OTC", "Cardano OTC", "Chainlink OTC", "Solana OTC", "TRON OTC", "Avalanche OTC", "Polygon OTC", "BNB OTC", "Bitcoin ETF OTC"],
    "Акции OTC": ["Apple OTC", "American Express OTC", "Microsoft OTC", "VISA OTC", "Amazon OTC", "Marathon Digital OTC", "Palantir OTC", "Coinbase OTC", "GameStop OTC", "Tesla OTC", "Netflix OTC", "Facebook OTC", "Google OTC", "NVIDIA OTC", "Intel OTC", "AMD OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#050505; color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:0;">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <div style="max-width:400px; margin:20px auto; padding:25px; background:#111; border:1px solid #222; border-radius:25px; text-align:center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <h2 style="color:#00d4ff; margin-bottom:20px; letter-spacing:1px;">QUANTUM CORE v4.2</h2>
        
        <select id="cat" onchange="upd()" style="width:100%; padding:14px; margin:8px 0; background:#1a1a1a; color:#fff; border:1px solid #333; border-radius:12px;"></select>
        <select id="asset" style="width:100%; padding:14px; margin:8px 0; background:#1a1a1a; color:#fff; border:1px solid #333; border-radius:12px;"></select>
        
        <div style="display:flex; gap:10px; margin-top:8px;">
            <select id="time" style="flex:1; padding:14px; background:#1a1a1a; color:#fff; border:1px solid #333; border-radius:12px;"></select>
            <select id="exp" style="flex:1; padding:14px; background:#1a1a1a; color:#fff; border:1px solid #333; border-radius:12px;"></select>
        </div>

        <button onclick="run()" style="width:100%; padding:16px; margin-top:20px; background:linear-gradient(90deg, #007bff, #00d4ff); border:none; color:white; font-weight:bold; border-radius:12px; font-size:16px; cursor:pointer;">ЗАПУСК АНАЛИЗА</button>
        
        <div id="res" style="font-size:40px; font-weight:800; margin:25px 0; color:#00ff00; height:50px;">--</div>
        <div id="timer" style="font-size:18px; color:#ffcc00; font-weight:bold; margin-bottom:15px;">--</div>
        
        <button id="mart" onclick="alert('Перекрытие активировано!')" style="display:none; width:100%; padding:14px; background:#2a1a1a; border:1px solid #ff4757; color:#ff4757; font-weight:bold; border-radius:12px; font-size:14px; cursor:pointer;">ПЕРЕКРЫТИЕ</button>

        <div id="tips" style="margin-top:25px; padding:15px; background:#1a1a1a; border-radius:15px; font-size:13px; color:#888; text-align:left; display:none;">
            <p><b>• Совет 1:</b> Не используй более 2-х перекрытий подряд.</p>
            <p><b>• Совет 2:</b> Следи за выходом новостей, волатильность может быть высокой.</p>
        </div>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        const times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"];
        
        function fillOptions(){
            times.forEach(t => {
                document.getElementById('time').innerHTML += `<option>${t}</option>`;
                document.getElementById('exp').innerHTML += `<option>${t}</option>`;
            });
        }
        
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
        
        fillOptions();
        upd();
        
        function run(){
            const sigs = ["ВВЕРХ", "ВНИЗ"];
            document.getElementById('res').innerText = sigs[Math.floor(Math.random()*2)];
            document.getElementById('mart').style.display = 'block';
            document.getElementById('tips').style.display = 'block';
            let t = 10;
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
    </script>
    </html>
    """
