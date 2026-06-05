import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# 70 активов
ASSETS = {
    "Валюты": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "EUR/JPY", "USD/CAD", "GBP/JPY", "NZD/USD", "USD/CHF", "EUR/GBP", "AUD/JPY", "CHF/JPY", "EUR/CAD", "EUR/NZD", "GBP/AUD", "GBP/CAD", "GBP/NZD", "NZD/CAD", "NZD/JPY", "USD/SGD", "USD/MXN", "USD/HKD", "USD/NOK", "USD/SEK", "USD/DKK", "EUR/NOK", "EUR/SEK", "EUR/DKK", "AUD/NZD", "AUD/CAD"],
    "Крипта": ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "DOT/USD", "XRP/USD", "LTC/USD", "BNB/USD", "TRX/USD", "DOGE/USD", "MATIC/USD", "LINK/USD", "AVAX/USD", "SHIB/USD", "UNI/USD", "XLM/USD", "ATOM/USD", "ALGO/USD", "FIL/USD", "VET/USD"],
    "Акции/OTC": ["AAPL", "TSLA", "NVDA", "AMZN", "GOOGL", "MSFT", "META", "NFLX", "AMD", "INTC", "Bitcoin OTC", "Ethereum OTC", "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "Gold OTC", "Silver OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:340px; margin:20px auto; padding:25px; background:#181818; border:2px solid #222; border-radius:20px; text-align:center;">
        <h2 style="color:#00ffcc;">QUANTUM CORE v4.2</h2>
        <select id="cat" onchange="upd()" style="width:100%; padding:10px; margin:5px; background:#111; color:#fff; border:1px solid #333;"></select>
        <select id="asset" style="width:100%; padding:10px; margin:5px; background:#111; color:#fff; border:1px solid #333;"></select>
        <select id="time" style="width:100%; padding:10px; margin:5px; background:#111; color:#fff; border:1px solid #333;">
            <option>5 сек</option><option>15 сек</option><option>30 сек</option><option>1 мин</option>
            <option>2 мин</option><option>3 мин</option><option>4 мин</option><option>5 мин</option>
            <option>6 мин</option><option>7 мин</option><option>8 мин</option><option>9 мин</option><option>10 мин</option>
        </select>
        <button onclick="run()" style="width:100%; padding:15px; background:linear-gradient(90deg, #007bff, #00d4ff); border:none; color:white; font-weight:bold; cursor:pointer; margin-top:15px; border-radius:5px;">ЗАПУСК АНАЛИЗА</button>
        <div id="res" style="font-size:32px; font-weight:900; margin:20px 0; color:#fff;">--</div>
        <div id="timer" style="font-size:18px; color:#ffcc00; font-weight:bold;">--</div>
        <button id="mart" onclick="alert('Перекрытие!')" style="display:none; width:100%; padding:12px; background:#ff4757; border:none; color:white; font-weight:bold; cursor:pointer; margin-top:15px; border-radius:5px;">ПЕРЕКРЫТИЕ</button>
    </div>
    <script>
        const data = """ + json.dumps(ASSETS) + """;
        function upd(){ let c=document.getElementById('cat').value; document.getElementById('asset').innerHTML = data[c].map(a => `<option>${a}</option>`).join(''); }
        Object.keys(data).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
        upd();
        function run(){
            const sigs = ["ВВЕРХ", "ВНИЗ"];
            document.getElementById('res').innerHTML = `<span style='color:#00ff00; font-size:36px'>${sigs[Math.floor(Math.random()*2)]}</span>`;
            document.getElementById('mart').style.display = 'block';
            let t = parseInt(document.getElementById('time').value);
            let i = setInterval(()=>{ t--; document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t + " сек"; if(t<=0) clearInterval(i); }, 1000);
        }
    </script>
    </html>
    """
