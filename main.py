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
    <html style="background:#f0f2f5; color:#1a1a1a; font-family:'Inter', sans-serif;">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <div style="max-width:420px; margin:20px auto; padding:25px; background:white; border-radius:35px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
        <h2 style="text-align:center; font-size:20px; margin-bottom:20px;">QUANTUM CORE v4.2</h2>
        
        <div style="margin-bottom:15px;">
            <label style="font-size:11px; font-weight:bold; color:#777; display:block; margin-bottom:5px;">КАТЕГОРИЯ</label>
            <select id="cat" onchange="upd()" style="width:100%; padding:12px; background:#f8f9fa; border:1px solid #eee; border-radius:12px;"></select>
        </div>
        
        <div style="margin-bottom:15px;">
            <label style="font-size:11px; font-weight:bold; color:#777; display:block; margin-bottom:5px;">АКТИВ</label>
            <select id="asset" style="width:100%; padding:12px; background:#f8f9fa; border:1px solid #eee; border-radius:12px;"></select>
        </div>
        
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <div style="flex:1;">
                <label style="font-size:11px; font-weight:bold; color:#777; display:block; margin-bottom:5px;">ИНТЕРВАЛ</label>
                <select id="time" style="width:100%; padding:12px; background:#f8f9fa; border:1px solid #eee; border-radius:12px;"></select>
            </div>
            <div style="flex:1;">
                <label style="font-size:11px; font-weight:bold; color:#777; display:block; margin-bottom:5px;">ЭКСПИРАЦИЯ</label>
                <select id="exp" style="width:100%; padding:12px; background:#f8f9fa; border:1px solid #eee; border-radius:12px;"></select>
            </div>
        </div>

        <button id="runBtn" onclick="run()" style="width:100%; padding:16px; background:#1a1a1a; border:none; color:white; font-weight:bold; border-radius:12px; cursor:pointer;">ЗАПУСК АНАЛИЗА</button>
        
        <div id="res" style="text-align:center; font-size:40px; font-weight:900; margin:20px 0;">--</div>
        <div id="timer" style="text-align:center; font-size:16px; font-weight:bold; color:#d9534f; margin-bottom:20px;">--</div>
        
        <button id="mart" onclick="run()" style="display:none; width:100%; padding:14px; background:#d9534f; color:white; font-weight:bold; border-radius:12px; border:none;">ПЕРЕКРЫТИЕ</button>

        <div style="margin-top:20px; font-size:12px; color:#666; background:#f8f9fa; padding:15px; border-radius:12px;">
            <p>• Не используйте более 2-х перекрытий.</p>
            <p>• Соблюдайте риск-менеджмент 1% от депозита.</p>
        </div>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        const times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"];
        
        function init(){
            times.forEach(t => { 
                document.getElementById('time').innerHTML += `<option>${t}</option>`;
                document.getElementById('exp').innerHTML += `<option>${t}</option>`;
            });
            Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
            upd();
        }
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        
        async function run(){
            const res = document.getElementById('res');
            document.getElementById('runBtn').disabled = true;
            res.innerText = "АНАЛИЗ...";
            res.style.color = "#555";
            await new Promise(r => setTimeout(r, 2000));
            
            const isUp = Math.random() > 0.5;
            res.innerText = isUp ? "ВВЕРХ" : "ВНИЗ";
            res.style.color = isUp ? "#28a745" : "#dc3545";
            
            document.getElementById('mart').style.display = 'block';
            document.getElementById('runBtn').disabled = false;
            
            let t = 10;
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
        init();
    </script>
    </html>
    """
