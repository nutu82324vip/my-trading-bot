import json
import random
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

signal_pool = []
def get_next_result():
    global signal_pool
    if not signal_pool:
        signal_pool = ["WIN"] * 100 + ["LOSS"] * 10
        random.shuffle(signal_pool)
    return signal_pool.pop()

# --- ВАШ ПОЛНЫЙ ОРИГИНАЛЬНЫЙ СЛОВАРЬ (БЕЗ СОКРАЩЕНИЙ) ---
ASSETS_DATA = {
    "ru": {
        "[ВСЕ АКТИВЫ] — OTC ЦИКЛ": {
            "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "АКЦИИ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "СЫРЬЕ / ИНДЕКСЫ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ВСЕ АКТИВЫ] — ЖИВОЙ РЫНОК": {
            "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "en": {
        "[ALL ASSETS] — OTC CYCLE": {
            "CURRENCY PAIRS": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "STOCKS": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "CRYPTOCURRENCY": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "COMMODITIES / INDICES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ALL ASSETS] — LIVE MARKET": {
            "CURRENCY PAIRS": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "ua": {
        "[ВСІ АКТИВИ] — OTC ЦИКЛ": {
            "ВАЛЮТНІ ПАРИ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "АКЦІЇ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "СИРОВИНА / ІНДЕКСИ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ВСІ АКТИВИ] — ЖИВИЙ РИНОК": {
            "ВАЛЮТНІ ПАРИ": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "es": {
        "[TODOS LOS ACTIVOS] — CICLO OTC": {
            "PARES DE DIVISAS": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "ACCIONES": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "CRIPTOMONEDAS": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "MATERIAS PRIMAS / ÍNDICES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[TODOS LOS ACTIVOS] — MERCADO EN VIVO": {
            "PARES DE DIVISAS": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "de": {
        "[ALLE VERMÖGENSWERTE] — OTC-ZYKLUS": {
            "WÄHRUNGSPAARE": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "AKTIEN": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "KRYPTOWÄHRUNG": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "ROHSTOFFE / INDIZES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ALLE VERMÖGENSWERTE] — LIVE-MARKT": {
            "WÄHRUNGSPAARE": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    }
}

@app.get("/get_signal")
async def get_signal(asset: str):
    outcome = get_next_result()
    await asyncio.sleep(1.0)
    return {"signal": random.choice(["UP", "DOWN"]), "accuracy": round(random.uniform(91, 98), 1), "outcome": outcome}

@app.get("/", response_class=HTMLResponse)
async def index():
    return f"""
    <html style="background:#06080c; color:#fff; font-family:sans-serif;">
    <div style="max-width:430px; margin:20px auto; padding:25px; background:#080a10; border-radius:28px; border:1px solid #1a2233; text-align:center;">
        
        <a href="https://t.me/+WB89-UHgktU0YmQy" target="_blank" style="text-decoration:none;">
            <button style="width:100%; padding:12px; background:linear-gradient(270deg, #ffd700, #ffa500); border:none; border-radius:10px; color:#000; font-weight:900; margin-bottom:10px; cursor:pointer;">👑 VIP СИГНАЛЫ</button>
        </a>
        <a href="https://t.me/SupportDev_Bot" target="_blank" style="text-decoration:none;">
            <button style="width:100%; padding:12px; background:#1a2233; border:1px solid #334466; border-radius:10px; color:#fff; font-weight:bold; margin-bottom:20px; cursor:pointer;">🛠 СВЯЗЬ С РАЗРАБОТЧИКОМ</button>
        </a>

        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <button onclick="updateStat('w', 1)" style="flex:1; background:#0f131e; border:1px solid #1a2233; color:#00ff66; padding:10px; border-radius:12px; cursor:pointer;">PROFIT: <span id="wc">0</span></button>
            <button onclick="updateStat('l', 1)" style="flex:1; background:#0f131e; border:1px solid #1a2233; color:#ff3344; padding:10px; border-radius:12px; cursor:pointer;">LOSS: <span id="lc">0</span></button>
        </div>
        <select id="lang" onchange="updateAssets()" style="width:100%; padding:10px; background:#0f131e; color:#fff; border-radius:10px;">
            <option value="ru">🇷🇺 RU</option><option value="en">🇺🇸 EN</option><option value="ua">🇺🇦 UA</option>
            <option value="es">🇪🇸 ES</option><option value="de">🇩🇪 DE</option>
        </select>
        <select id="asset" style="width:100%; margin:10px 0; padding:10px; background:#0f131e; color:#fff; border-radius:10px;"></select>
        <button id="runBtn" onclick="startProcess(false)" style="width:100%; padding:15px; background:#641bfa; color:#fff; border:none; border-radius:10px; cursor:pointer; font-weight:800;">СКАНИРОВАТЬ (10с)</button>
        <button id="aiBtn" onclick="startProcess(true)" style="width:100%; padding:15px; background:#00b344; color:#000; border:none; border-radius:10px; cursor:pointer; margin-top:10px; font-weight:900;">ИИ СДЕЛАТЬ ЗА ВАС (25с)</button>
        <div id="res" style="font-size:50px; font-weight:900; margin:20px 0;">--</div>
        <div id="timer" style="color:#ffaa00; font-weight:bold; height:20px;">--</div>
        <button id="mart" style="display:none; width:100%; padding:15px; background:#ff3344; color:#fff; border:none; border-radius:10px; cursor:pointer; margin-top:20px;" onclick="startProcess(false)">ПЕРЕКРЫТИЕ (MARTINGALE)</button>
    </div>
    <script>
        const data = {json.dumps(ASSETS_DATA)};
        let w=0, l=0, timer=null;
        function updateStat(t, v) {{ t=='w'?(w+=v, document.getElementById('wc').innerText=w):(l+=v, document.getElementById('lc').innerText=l); }}
        function updateAssets() {{
            let l = document.getElementById('lang').value;
            let sel = document.getElementById('asset');
            sel.innerHTML = "";
            Object.keys(data[l]).forEach(cat => {{
                Object.values(data[l][cat]).forEach(arr => arr.forEach(a => sel.innerHTML += `<option>${{a}}</option>`));
            }});
        }}
        async function startProcess(isAI) {{
            document.getElementById('mart').style.display = 'none';
            let asset = isAI ? document.querySelectorAll('option')[Math.floor(Math.random()*10)].value : document.getElementById('asset').value;
            let res = await (await fetch('/get_signal?asset='+asset)).json();
            document.getElementById('res').innerText = res.signal;
            document.getElementById('res').style.color = res.signal=="UP" ? "#00ff66" : "#ff3344";
            let s = isAI ? 25 : 10;
            if(timer) clearInterval(timer);
            timer = setInterval(() => {{
                document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + s;
                if(s-- <= 0) {{
                    clearInterval(timer);
                    document.getElementById('timer').innerText = "ИДЕТ СДЕЛКА (60с)...";
                    let e = 60;
                    let exp = setInterval(() => {{
                        if(e-- <= 0) {{ clearInterval(exp); document.getElementById('timer').innerText = "СДЕЛКА ЗАКРЫТА"; document.getElementById('mart').style.display = 'block'; }}
                    }}, 1000);
                }}
            }}, 1000);
        }}
        updateAssets();
    </script>
    </html>
    """
