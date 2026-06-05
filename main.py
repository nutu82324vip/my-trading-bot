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
    <div style="max-width:420px; margin:20px auto; padding:30px; background:white; border-radius:35px; box-shadow: 0 20px 40px rgba(0,0,0,0.08); text-align:center;">
        <h2 style="font-size:22px; margin-bottom:20px;">QUANTUM CORE v4.2</h2>
        
        <div style="text-align:left; font-size:12px; font-weight:bold; color:#555; margin-bottom:5px;">КАТЕГОРИЯ</div>
        <select id="cat" onchange="upd()" style="width:100%; padding:15px; margin-bottom:15px; background:#f8f9fa; border:none; border-radius:15px;"></select>
        
        <div style="text-align:left; font-size:12px; font-weight:bold; color:#555; margin-bottom:5px;">АКТИВ</div>
        <select id="asset" style="width:100%; padding:15px; margin-bottom:15px; background:#f8f9fa; border:none; border-radius:15px;"></select>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-bottom:20px;">
            <div>
                <div style="text-align:left; font-size:11px; font-weight:bold; color:#555; margin-bottom:5px;">ИНТЕРВАЛ</div>
                <select id="time" style="width:100%; padding:15px; background:#f8f9fa; border:none; border-radius:15px;"></select>
            </div>
            <div>
                <div style="text-align:left; font-size:11px; font-weight:bold; color:#555; margin-bottom:5px;">ЭКСПИРАЦИЯ</div>
                <select id="exp" style="width:100%; padding:15px; background:#f8f9fa; border:none; border-radius:15px;"></select>
            </div>
        </div>

        <button id="runBtn" onclick="run()" style="width:100%; padding:18px; background:#1a1a1a; border:none; color:white; font-weight:bold; border-radius:15px; cursor:pointer; font-size:16px;">ЗАПУСК АНАЛИЗА</button>
        
        <div id="res" style="font-size:48px; font-weight:800; margin:25px 0; color:#1a1a1a;">--</div>
        <div id="timer" style="font-size:18px; font-weight:bold; margin-bottom:20px; color:#d9534f;">--</div>
        
        <button id="mart" onclick="activateMart()" style="display:none; width:100%; padding:15px; background:white; border:2px solid #d9534f; color:#d9534f; font-weight:bold; border-radius:15px; transition:0.3s;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        const options = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "6 мин", "7 мин", "8 мин", "9 мин", "10 мин"];
        
        function init(){
            options.forEach(o => {
                document.getElementById('time').innerHTML += `<option>${o}</option>`;
                document.getElementById('exp').innerHTML += `<option>${o}</option>`;
            });
            Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
            upd();
        }
        
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        
        function activateMart(){
            const btn = document.getElementById('mart');
            btn.style.background = "#d9534f";
            btn.style.color = "white";
            btn.innerText = "ПЕРЕКРЫТИЕ АКТИВИРОВАНО";
        }
        
        async function run(){
            const btn = document.getElementById('runBtn');
            btn.disabled = true;
            btn.innerText = "АНАЛИЗ...";
            document.getElementById('res').innerText = "...";
            await new Promise(r => setTimeout(r, 3000));
            
            document.getElementById('res').innerText = Math.random() > 0.5 ? "ВВЕРХ" : "ВНИЗ";
            const martBtn = document.getElementById('mart');
            martBtn.style.display = 'block';
            martBtn.style.background = "white";
            martBtn.style.color = "#d9534f";
            martBtn.innerText = "ПЕРЕКРЫТИЕ";
            
            btn.disabled = false;
            btn.innerText = "ЗАПУСК АНАЛИЗА";
            
            let t = 10;
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
        init();
    </script>
    </html>
    """
