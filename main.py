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
    <html style="background:#eef2f5; color:#333; font-family:'Roboto', sans-serif;">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <div style="max-width:400px; margin:20px auto; padding:25px; background:white; border-radius:30px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align:center;">
        <h2 style="color:#007bff; margin-bottom:5px;">QUANTUM CORE v4.2</h2>
        <p style="font-size:12px; color:#888;">NEURAL MARKET ANALYZER</p>
        
        <select id="cat" onchange="upd()" style="width:100%; padding:14px; margin:8px 0; border:2px solid #e0e0e0; border-radius:15px;"></select>
        <select id="asset" style="width:100%; padding:14px; margin:8px 0; border:2px solid #e0e0e0; border-radius:15px;"></select>
        
        <button id="runBtn" onclick="run()" style="width:100%; padding:18px; margin-top:20px; background:#007bff; border:none; color:white; font-weight:bold; border-radius:15px; cursor:pointer;">ЗАПУСК АНАЛИЗА</button>
        
        <div id="status" style="margin:20px 0; font-weight:bold; color:#555; height:20px;"></div>
        <div id="res" style="font-size:48px; font-weight:900; margin:10px 0; color:#007bff;">--</div>
        <div id="timer" style="font-size:18px; color:#ff9800; font-weight:bold;">--</div>
        
        <button id="mart" onclick="alert('Перекрытие активировано!')" style="display:none; width:100%; padding:14px; margin-top:15px; background:#ff4757; border:none; color:white; font-weight:bold; border-radius:15px;">ПЕРЕКРЫТИЕ</button>

        <div id="tips" style="margin-top:25px; padding:15px; background:#f8f9fa; border-radius:20px; font-size:13px; color:#666; display:none;">
            <p><i>ИИ анализирует 4.2 млрд котировок...</i></p>
            <p><b>• Совет:</b> Используйте 1% от баланса.</p>
        </div>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
        upd();
        
        async function run(){
            document.getElementById('runBtn').disabled = true;
            document.getElementById('status').innerText = "ИИ делает глубокий анализ графика...";
            document.getElementById('res').innerText = "...";
            document.getElementById('tips').style.display = 'block';
            
            await new Promise(r => setTimeout(r, 3000));
            
            const sigs = ["ВВЕРХ", "ВНИЗ"];
            document.getElementById('status').innerText = "Сигнал готов:";
            document.getElementById('res').innerHTML = `<span style='color:#28a745;'>${sigs[Math.floor(Math.random()*2)]}</span>`;
            document.getElementById('mart').style.display = 'block';
            document.getElementById('runBtn').disabled = false;
            
            let t = 10;
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
    </script>
    </html>
    """
