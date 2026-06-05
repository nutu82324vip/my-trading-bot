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
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif; margin:0; padding:0;">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <div style="max-width:400px; margin:20px auto; padding:20px; background:#121212; border:1px solid #333; border-radius:15px; text-align:center;">
        <h2 style="color:#00d4ff;">QUANTUM CORE v4.2</h2>
        <select id="cat" onchange="upd()" style="width:100%; padding:10px; margin:5px 0; background:#1e1e1e; color:#fff; border:1px solid #444;"></select>
        <select id="asset" style="width:100%; padding:10px; margin:5px 0; background:#1e1e1e; color:#fff; border:1px solid #444;"></select>
        <div style="display:flex; gap:5px;">
            <select id="time" style="width:50%; padding:10px; background:#1e1e1e; color:#fff; border:1px solid #444;">
                <option>5 сек</option><option>15 сек</option><option>30 сек</option>
                <option>1 мин</option><option>2 мин</option><option>3 мин</option><option>4 мин</option>
                <option>5 мин</option><option>6 мин</option><option>7 мин</option><option>8 мин</option>
                <option>9 мин</option><option>10 мин</option>
            </select>
            <select id="exp" style="width:50%; padding:10px; background:#1e1e1e; color:#fff; border:1px solid #444;">
                <option>5 сек</option><option>15 сек</option><option>30 сек</option>
                <option>1 мин</option><option>2 мин</option><option>3 мин</option><option>4 мин</option>
                <option>5 мин</option><option>6 мин</option><option>7 мин</option><option>8 мин</option>
                <option>9 мин</option><option>10 мин</option>
            </select>
        </div>
        <button onclick="run()" style="width:100%; padding:15px; margin-top:15px; background:#007bff; border:none; color:white; font-weight:bold; border-radius:5px;">ЗАПУСК АНАЛИЗА</button>
        <div id="res" style="font-size:30px; font-weight:bold; margin:15px 0; color:#fff;">--</div>
        <div id="timer" style="font-size:18px; color:#ffcc00; margin-bottom:10px;">--</div>
        <button id="mart" onclick="alert('Перекрытие активировано!')" style="display:none; width:100%; padding:12px; background:#ff4757; border:none; color:white; font-weight:bold; border-radius:5px;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
        upd();
        function run(){
            const sigs = ["ВВЕРХ", "ВНИЗ"];
            document.getElementById('res').innerHTML = `<span style='color:#00ff00;'>${sigs[Math.floor(Math.random()*2)]}</span>`;
            document.getElementById('mart').style.display = 'block';
            let t = 10; // Отсчет до входа
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
    </script>
    </html>
    """
