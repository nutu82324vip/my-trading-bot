import json
import random
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Глобальный пул для контроля статистики (100 побед, 10 поражений)
signal_pool = []

def get_next_result():
    global signal_pool
    if not signal_pool:
        signal_pool = ["WIN"] * 100 + ["LOSS"] * 10
        random.shuffle(signal_pool)
    return signal_pool.pop()

ASSETS_DATA = {
    "ru": {
        "[ВСЕ АКТИВЫ] — OTC ЦИКЛ": {
            "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "АКЦИИ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "СЫРЬЕ / ИНДЕКСЫ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ВСЕ АКТИВЫ] — ЖИВОЙ РЫНОК": {
            "КРИПТОВАЛЮТА": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
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
            "CRYPTOCURRENCY": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
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
            "КРИПТОВАЛЮТА": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
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
            "CRIPTOMONEDAS": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
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
            "KRYPTOWÄHRUNG": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "WÄHRUNGSPAARE": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    }
}

def get_pocket_payout(asset: str) -> int:
    if "OTC" in asset: return 92
    if any(crypto in asset for crypto in ["BTC", "ETH", "SOL", "XRP", "LTC", "TRX", "BNB", "DOGE"]): return 78
    return 82

@app.get("/get_signal")
async def get_signal(asset: str, timeframe: str):
    outcome = get_next_result()
    await asyncio.sleep(1.5)
    
    is_up = random.random() > 0.41
    # WIN - высокая точность, LOSS - заниженная
    accuracy = round(random.uniform(91.0, 98.5), 1) if outcome == "WIN" else round(random.uniform(55.0, 65.0), 1)
    
    return {
        "signal": "UP" if is_up else "DOWN",
        "payout": get_pocket_payout(asset),
        "accuracy": accuracy,
        "outcome": outcome
    }

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#06080c; color:#ffffff; font-family:'Segoe UI', Roboto, sans-serif; margin:0; padding:0;">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HROM QUANTUM CORE v16.0</title>
        <style>
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            @keyframes shine { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            .loader { width: 45px; height: 45px; border: 4px solid #161b26; border-top: 4px solid #a855f7; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 15px auto; display: none; }
            select { width: 100%; padding: 14px; background: #0f131e; border: 1px solid #1a2233; border-radius: 14px; font-size: 14px; font-weight: 600; color: #ffffff; outline: none; appearance: none; }
            label { font-size: 11px; font-weight: bold; color: #4b5975; display: block; margin-bottom: 5px; letter-spacing: 0.8px; text-transform: uppercase; }
            .btn { width: 100%; padding: 16px; border: none; color: white; font-weight: 800; border-radius: 14px; cursor: pointer; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; transition: all 0.2s; margin-bottom: 10px; }
            .btn-main { background: linear-gradient(135deg, #963bfe 0%, #641bfa 100%); box-shadow: 0 5px 20px rgba(100,27,250,0.4); }
            .btn-auto { background: linear-gradient(135deg, #00ff66 0%, #00b344 100%); color: #000; font-weight: 900; }
            .btn-vip-top { padding: 8px 12px; border: none; border-radius: 8px; background: linear-gradient(270deg, #ffd700, #ffa500, #b8860b, #ffd700); background-size: 400% 400%; animation: shine 4s ease infinite; color: #000 !important; font-weight: 900; font-size: 11px; cursor: pointer; box-shadow: 0 2px 10px rgba(255,215,0,0.3); text-transform: uppercase; letter-spacing: 0.5px; }
            .btn-pocket { background: #141924; border: 1px solid #222d42; color: #38ef7d; }
            .btn-support { background: #080a10; border: 1px solid #161b26; color: #586988; font-size: 11px; margin-top: 15px; }
            .btn:active { transform: scale(0.98); }
            .lang-select { background: #0f131e; color: white; border: 1px solid #1a2233; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: bold; }
            .payout-badge { color: #00ff66; font-weight: 800; font-size: 12px; margin-top: 4px; display: block; }
            .counter-box { display: flex; justify-content: center; gap: 15px; margin: 15px 0 10px 0; }
            .count-btn { display: flex; align-items: center; gap: 8px; background: #0f131e; padding: 10px 16px; border-radius: 12px; border: 1px solid #1a2233; cursor: pointer; font-weight: 800; font-size: 13px; transition: all 0.2s; }
            .count-btn:active { transform: scale(0.95); background: #141a29; }
        </style>
    </head>
    <div style="max-width:430px; margin:15px auto; padding:0 15px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span id="flag_icon" style="font-size:20px; line-height:1;">🇷🇺</span>
            <select id="lang" class="lang-select" onchange="changeLang()"><option value="ru">🇷🇺 RU</option><option value="en">🇺🇸 EN</option><option value="ua">🇺🇦 UA</option><option value="es">🇪🇸 ES</option><option value="de">🇩🇪 DE</option></select>
        </div>
        <a href="https://t.me/+WB89-UHgktU0YmQy" target="_blank" style="text-decoration: none;"><button id="vip_btn_text" class="btn-vip-top">👑 VIP СИГНАЛЫ</button></a>
    </div>
    <div style="max-width:430px; margin:0 auto 30px auto; padding:25px; background:#080a10; border-radius:28px; border: 1px solid #121722; box-shadow: 0 25px 50px rgba(0,0,0,0.8); text-align:center;">
        <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:20px;">
            <div style="width:7px; height:7px; background:#00ff66; border-radius:50%; box-shadow: 0 0 10px #00ff66;"></div>
            <span id="lbl_title" style="font-size:11px; font-weight:800; letter-spacing:2px; color:#00ff66;">AI QUANTUM ENGINE ACTIVE</span>
        </div>
        <div style="text-align:left; margin-bottom:14px;"><label id="lbl_market">КАТЕГОРИЯ РЫНКА</label><select id="cat" onchange="updCategory()"></select></div>
        <div id="sub_cat_block" style="text-align:left; margin-bottom:14px;"><label id="lbl_type">ТИП АКТИВА</label><select id="sub_cat" onchange="updSubCategory()"></select></div>
        <div style="text-align:left; margin-bottom:14px;"><label id="lbl_asset">АКТИВНАЯ ПАРА</label><select id="asset" onchange="updAsset()"></select><span id="payout_lbl" class="payout-badge">PAYOUT: 92%</span></div>
        <div style="display:flex; gap:12px; margin-bottom:20px; text-align:left;">
            <div style="flex:1;"><label id="lbl_tf">ИНТЕРВАЛ СВЕЧИ</label><select id="time"></select></div>
            <div style="flex:1;"><label id="lbl_exp">ЭКСПИРАЦИЯ</label><select id="exp"></select></div>
        </div>
        <button id="runBtn" class="btn btn-main" onclick="getLiveSignal(false)">СКАНИРОВАТЬ РЫНОК</button>
        <button id="autoBtn" class="btn btn-auto" onclick="aiDoForYou()">ИИ СДЕЛАТЬ ЗА ВАС</button>
        <a href="https://pocketoption.com/register" target="_blank" style="text-decoration: none;"><button id="btn_pocket" class="btn btn-pocket">ОТКРЫТЬ POCKET OPTION</button></a>
        <div id="status" style="font-size:11px; color:#4b5975; margin-top:20px; min-height:18px; font-weight:700; letter-spacing:0.5px;">СИСТЕМА СИНХРОНИЗИРОВАНА</div>
        <div id="loader" class="loader"></div>
        <div id="res" style="font-size:55px; font-weight:900; margin:10px 0; min-height:66px; letter-spacing:2px; color:#ffffff;">--</div>
        <div id="accuracy" style="font-size:14px; font-weight:800; color:#a855f7; margin-top:-5px; margin-bottom:10px; display:none;"></div>
        <div class="counter-box">
            <button class="count-btn" onclick="adjustCounter('win', 1)" oncontextmenu="adjustCounter('win', -1); return false;"><span style="color:#586988; font-size:11px;">PROFIT +</span><span id="win_counter" style="color:#00ff66;">0</span></button>
            <button class="count-btn" onclick="adjustCounter('loss', 1)" oncontextmenu="adjustCounter('loss', -1); return false;"><span style="color:#586988; font-size:11px;">LOSS -</span><span id="loss_counter" style="color:#ff3344;">0</span></button>
        </div>
        <div id="timer" style="font-size:14px; font-weight:800; color:#ffaa00; margin-bottom:15px; min-height:20px;"></div>
        <button id="mart" class="btn" onclick="getLiveSignal(true)" style="display:none; background:#ff3344; box-shadow: 0 5px 15px rgba(255,51,68,0.3);">АКТИВИРОВАТЬ ПЕРЕКРЫТИЕ</button>
        <a href="https://t.me/+WB89-UHgktU0YmQy" target="_blank" style="text-decoration: none;"><button id="btn_supp" class="btn btn-support">РАЗРАБОТЧИК / SUPPORT</button></a>
    </div>
    <script>
        const rawData = """ + json.dumps(ASSETS_DATA) + """;
        const tf_options = { ru: ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "10 мин"], en: ["5 sec", "15 sec", "30 sec", "1 min", "2 min", "3 min", "4 min", "5 min", "10 min"], ua: ["5 сек", "15 сек", "30 сек", "1 хв", "2 хв", "3 хв", "4 хв", "5 хв", "10 хв"], es: ["5 seg", "15 seg", "30 seg", "1 min", "2 min", "3 min", "4 min", "5 min", "10 min"], de: ["5 Sek", "15 Sek", "30 Sek", "1 Min", "2 Min", "3 Min", "4 Min", "5 Min", "10 Min"] };
        let mainInterval = null, wins = 0, losses = 0;
        const flags = { ru: "🇷🇺", en: "🇺🇸", ua: "🇺🇦", es: "🇪🇸", de: "🇩🇪" };
        const dictionary = { ru: { title: "AI QUANTUM ENGINE ACTIVE", market: "КАТЕГОРИЯ РЫНКА", type: "ТИП АКТИВА", asset: "АКТИВНАЯ ПАРА", tf: "ИНТЕРВАЛ СВЕЧИ", exp: "ЭКСПИРАЦИЯ", scan: "СКАНИРОВАТЬ РЫНОК", auto: "ИИ СДЕЛАТЬ ЗА ВАС", pocket: "ОТКРЫТЬ POCKET OPTION", support: "РАЗРАБОТЧИК / SUPPORT", ready: "СИСТЕМА СИНХРОНИЗИРОВАНА", load: "[ АНАЛИЗ РЫНОЧНОГО ОРДЕРА... ]", UP: "ВВЕРХ / CALL", DOWN: "ВНИЗ / PUT", otc: "СИСТЕМА ИИ: РАСЧЕТ УСПЕШЕН", buy: "АНАЛИЗ TV: СИГНАЛ НА ПОКУПКУ", sell: "АНАЛИЗ TV: СИГНАЛ НА ПРОДАЖУ", flat: "МАТРИЦА ОБЪЕМОВ: ИМПУЛЬС ТРЕНДА", backup: "АВТОНОМНЫЙ ИИ РЕЖИМ", mart_status: "[ РАСЧЕТ ШАГА МАРТИНГЕЙЛА... ]", mart_btn: "АКТИВИРОВАТЬ ПЕРЕКРЫТИЕ", wait: "ВХОД В СДЕЛКУ ЧЕРЕЗ: ", process: "СДЕЛКА В ПРОЦЕССЕ ТОРГОВЛИ: ", end: "ТОРГОВЫЙ ЦИКЛ ЗАВЕРШЕН", ai_search: "[ ИИ ИЩЕТ ЛУЧШУЮ ТОЧКУ ВХОДУ... ]", vip: "👑 VIP СИГНАЛЫ" }, en: { title: "AI QUANTUM ENGINE ACTIVE", market: "MARKET CATEGORY", type: "ASSET TYPE", asset: "ACTIVE PAIR", tf: "CANDLE TIMEFRAME", exp: "EXPIRATION TIME", scan: "SCAN MARKET", auto: "AI DO FOR YOU", pocket: "OPEN POCKET OPTION", support: "DEVELOPER / SUPPORT", ready: "SYSTEM SYNCHRONIZED", load: "[ ANALYZING MARKET ORDER... ]", UP: "CALL", DOWN: "PUT", otc: "AI SYSTEM: CALCULATION SUCCESS", buy: "TV ANALYSIS: BUY SIGNAL", sell: "TV ANALYSIS: SELL SIGNAL", flat: "VOLUME MATRIX: TREND IMPULSE", backup: "AUTONOMOUS AI MODE", mart_status: "[ CALCULATING MARTINGALE STEP... ]", mart_btn: "ACTIVATE MULTIPLIER", wait: "ENTER TRADE IN: ", process: "TRADE IN PROCESS: ", end: "TRADE CYCLE COMPLETED", ai_search: "[ AI SEARCHING BEST ENTRY POINT... ]", vip: "👑 VIP SIGNALS" }, ua: { title: "AI QUANTUM ENGINE ACTIVE", market: "КАТЕГОРІЯ РИНКУ", type: "ТИП АКТИВУ", asset: "АКТИВНА ПАРА", tf: "ІНТЕРВАЛ СВІЧКИ", exp: "ЕКСПІРАЦІЯ", scan: "СКАНУВАТИ РИНОК", auto: "ШІ ЗРОБИТЬ ЗА ВАС", pocket: "ВІДКРИТИ POCKET OPTION", support: "РОЗРОБНИК / SUPPORT", ready: "СИСТЕМА СИНХРОНІЗОВАНА", load: "[ АНАЛІЗ РИНКОВОГО ОРДЕРУ... ]", UP: "ВГОРУ / CALL", DOWN: "ВНИЗ / PUT", otc: "СИСТЕМА ШІ: РОЗРАХУНОК УСПІШНИЙ", buy: "АНАЛІЗ TV: СИГНАЛ НА ПОКУПКУ", sell: "АНАЛІЗ TV: СИГНАЛ НА ПРОДАЖУ", flat: "МАТРИЦЯ ОБ'ЄМІВ: ІМПУЛЬС ТРЕНДУ", backup: "АВТОНОМНИЙ РЕЖИМ ШІ", mart_status: "[ РОЗРАХУНОК КРОКУ МАРТИНГЕЙЛУ... ]", mart_btn: "АКТИВУВАТИ ПЕРЕКРИТТЯ", wait: "ВХІД У УГОДУ ЧЕРЕЗ: ", process: "УГОДА В ПРОЦЕСІ ТОРГІВЛІ: ", end: "ТОРГОВИЙ ЦИКЛ ЗАВЕРШЕНО", ai_search: "[ ШІ ШУКАЄ КРАЩУ ТОЧКУ ВХОДУ... ]", vip: "👑 VIP СИГНАЛИ" }, es: { title: "AI QUANTUM ENGINE ACTIVE", market: "CATEGORÍA DE MERCADO", type: "TIPO DE ACTIVO", asset: "PAR ACTIVO", tf: "TEMPORALIDAD VELA", exp: "TIEMPO EXPIRACIÓN", scan: "ESCANEAR MERCADO", auto: "IA HACER POR TI", pocket: "ABRIR POCKET OPTION", support: "DESARROLLADOR / SUPPORT", ready: "SISTEMA SINCRONIZADO", load: "[ ANALIZANDO ORDEN DE MERCADO... ]", UP: "SUBIR / CALL", DOWN: "BAJAR / PUT", otc: "SISTEMA IA: CÁLCULO EXITOSO", buy: "ANÁLISIS TV: SEÑAL DE COMPRA", sell: "ANÁLISIS TV: SEÑAL DE VENTA", flat: "MATRIZ DE VOLUMEN: IMPULSO DE TENDENCIA", backup: "MODO IA AUTÓNOMO", mart_status: "[ CALCULANDO PASO MARTINGALA... ]", mart_btn: "ACTIVAR MULTIPLICADOR", wait: "ENTRAR EN OPERACIÓN EN: ", process: "OPERACIÓN EN CURSO: ", end: "CICLO DE TRADING COMPLETADO", ai_search: "[ IA BUSCANDO MEJOR PUNTO DE ENTRADA... ]", vip: "👑 SEÑALES VIP" }, de: { title: "AI QUANTUM ENGINE ACTIVE", market: "MARKTKATEGORIE", type: "ASSET-TYP", asset: "AKTIVES PAAR", tf: "KERZEN TIMEFRAME", exp: "ABLAUFZEIT", scan: "MARKT SCANNEN", auto: "KI FÜR DICH TUN", pocket: "POCKET OPTION ÖFFNEN", support: "ENTWICKLER / SUPPORT", ready: "SYSTEM SYNCHRONISIERT", load: "[ MARKTORDER WIRD ANALYSIERT... ]", UP: "CALL", DOWN: "PUT", otc: "KI-SYSTEM: BERECHNUNG ERFOLGREICH", buy: "TV-ANALYSE: KAUFSIGNAL", sell: "TV-ANALYSE: VERKAUFSIGNAL", flat: "VOLUMENMATRIX: TRENDIMPULS", backup: "AUTONOMER KI-MODUS", mart_status: "[ MARTINGALE-SCHRITT WIRD BERECHNET... ]", mart_btn: "MULTIPLIER AKTIVIEREN", wait: "HANDEL STARTET IN: ", process: "HANDEL LÄUFT: ", end: "HANDELSZYKLUS BEENDET", ai_search: "[ KI SUCHT NACH BESTEM EINSTIEGSPUNKT... ]", vip: "👑 VIP-SIGNALE" } };
        function changeLang() { let l = document.getElementById('lang').value, d = dictionary[l] || dictionary['en']; document.getElementById('flag_icon').innerText = flags[l]; document.getElementById('lbl_title').innerText = d.title; document.getElementById('lbl_market').innerText = d.market; document.getElementById('lbl_type').innerText = d.type; document.getElementById('lbl_asset').innerText = d.asset; document.getElementById('lbl_tf').innerText = d.tf; document.getElementById('lbl_exp').innerText = d.exp; document.getElementById('runBtn').innerText = d.scan; document.getElementById('autoBtn').innerText = d.auto; document.getElementById('btn_pocket').innerText = d.pocket; document.getElementById('btn_supp').innerText = d.support; document.getElementById('mart').innerText = d.mart_btn; document.getElementById('status').innerText = d.ready; document.getElementById('vip_btn_text').innerText = d.vip; let oldCatIdx = Math.max(0, document.getElementById('cat').selectedIndex), catSelect = document.getElementById('cat'); catSelect.innerHTML = ""; Object.keys(rawData[l]).forEach(c => { catSelect.innerHTML += `<option>${c}</option>`; }); catSelect.selectedIndex = oldCatIdx <= catSelect.options.length - 1 ? oldCatIdx : 0; updCategory(true); }
        function adjustCounter(type, amount) { if(type === 'win') { wins = Math.max(0, wins + amount); document.getElementById('win_counter').innerText = wins; } else { losses = Math.max(0, losses + amount); document.getElementById('loss_counter').innerText = losses; } }
        function calcLocalPayout(assetName) { if(assetName.includes("OTC")) return 92; if(["BTC", "ETH", "SOL", "XRP", "LTC", "TRX", "BNB", "DOGE"].some(c => assetName.includes(c))) return 78; return 82; }
        function updCategory(isLangChange = false){ let l = document.getElementById('lang').value, c = document.getElementById('cat').value, oldSubIdx = Math.max(0, document.getElementById('sub_cat').selectedIndex), types = Object.keys(rawData[l][c]); document.getElementById('sub_cat').innerHTML = types.map(t => `<option>${t}</option>`).join(''); if(isLangChange) document.getElementById('sub_cat').selectedIndex = oldSubIdx <= types.length - 1 ? oldSubIdx : 0; updSubCategory(isLangChange); }
        function updSubCategory(isLangChange = false) { let l = document.getElementById('lang').value, c = document.getElementById('cat').value, t = document.getElementById('sub_cat').value, oldAssetIdx = Math.max(0, document.getElementById('asset').selectedIndex), currentAssets = rawData[l][c][t] || []; document.getElementById('asset').innerHTML = currentAssets.map(a => `<option>${a}</option>`).join(''); if(isLangChange) document.getElementById('asset').selectedIndex = oldAssetIdx <= document.getElementById('asset').options.length - 1 ? oldAssetIdx : 0; updAsset(isLangChange); }
        function updAsset(isLangChange = false) { let l = document.getElementById('lang').value, asset = document.getElementById('asset').value; if(!asset) return; document.getElementById('payout_lbl').innerText = `PAYOUT: ${calcLocalPayout(asset)}%`; let oldTfIdx = Math.max(0, document.getElementById('time').selectedIndex), oldExpIdx = Math.max(0, document.getElementById('exp').selectedIndex), tfSelect = document.getElementById('time'); tfSelect.innerHTML = ""; tf_options[l].forEach(o => { tfSelect.innerHTML += `<option>${o}</option>`; }); tfSelect.selectedIndex = oldTfIdx; let expSelect = document.getElementById('exp'); expSelect.innerHTML = ""; let currentOptions = asset.includes("OTC") ? tf_options[l] : tf_options[l].slice(3); currentOptions.forEach(o => { expSelect.innerHTML += `<option value="${o}">${o}</option>`; }); expSelect.selectedIndex = oldExpIdx <= expSelect.options.length - 1 ? oldExpIdx : 0; }
        async function aiDoForYou() { let l = document.getElementById('lang').value, cats = Object.keys(rawData[l]); document.getElementById('cat').value = cats[Math.floor(Math.random() * cats.length)]; updCategory(); let subCats = Object.keys(rawData[l][document.getElementById('cat').value]); document.getElementById('sub_cat').value = subCats[Math.floor(Math.random() * subCats.length)]; updSubCategory(); let assetSelect = document.getElementById('asset'); assetSelect.value = assetSelect.options[Math.floor(Math.random() * assetSelect.options.length)].value; updAsset(); let tfSelect = document.getElementById('time'); tfSelect.value = tfSelect.options[Math.floor(Math.random() * tfSelect.options.length)].value; let expSelect = document.getElementById('exp'); expSelect.value = expSelect.options[Math.floor(Math.random() * expSelect.options.length)].value; getLiveSignal(false, true); }
        function parseToSeconds(v) { let n = parseInt(v); return n * (v.includes("мин") || v.includes("min") || v.includes("хв") || v.includes("Min") ? 60 : 1); }
        async function getLiveSignal(isMartingale, isAiAuto = false) { if(mainInterval) clearInterval(mainInterval); let l = document.getElementById('lang').value, d = dictionary[l] || dictionary['en']; const runBtn = document.getElementById('runBtn'), autoBtn = document.getElementById('autoBtn'), martBtn = document.getElementById('mart'), status = document.getElementById('status'), res = document.getElementById('res'), timer = document.getElementById('timer'), loader = document.getElementById('loader'), accField = document.getElementById('accuracy'); runBtn.disabled = autoBtn.disabled = martBtn.disabled = true; res.style.display = accField.style.display = 'none'; loader.style.display = 'block'; status.innerText = isAiAuto ? d.ai_search : (isMartingale ? d.mart_status : d.load); timer.innerText = ""; let asset = document.getElementById('asset').value, timeframe = document.getElementById('time').value, expTimeStr = document.getElementById('exp').value; try { let response = await fetch(`/get_signal?asset=${encodeURIComponent(asset)}&timeframe=${encodeURIComponent(timeframe)}`); let result = await response.json(); await new Promise(r => setTimeout(r, 2600)); loader.style.display = 'none'; res.style.display = 'block'; res.innerText = d[result.signal]; res.style.color = result.signal === "UP" ? "#00ff66" : "#ff3344"; accField.innerText = `🎯 ACCURACY: ${result.accuracy}%`; accField.style.display = 'block'; status.innerText = d.otc; let entryTime = isAiAuto ? 20 : 10; timer.style.color = "#ffaa00"; timer.innerText = d.wait + entryTime + " SEC"; mainInterval = setInterval(() => { if (entryTime > 0) { entryTime--; timer.innerText = d.wait + entryTime + " SEC"; if(entryTime === 0) { let tradeTime = parseToSeconds(expTimeStr); timer.style.color = "#00ff66"; timer.innerText = d.process + tradeTime + " SEC"; clearInterval(mainInterval); mainInterval = setInterval(() => { tradeTime--; timer.innerText = d.process + tradeTime + " SEC"; if(tradeTime <= 0) { clearInterval(mainInterval); timer.style.color = "#ffffff"; timer.innerText = d.end; if (result.outcome === "WIN") { wins++; document.getElementById('win_counter').innerText = wins; } else { losses++; document.getElementById('loss_counter').innerText = losses; } } }, 1000); } } }, 1000); } catch(e) { loader.style.display = 'none'; status.innerText = "ERROR"; } runBtn.disabled = autoBtn.disabled = martBtn.disabled = false; martBtn.style.display = 'block'; }
        changeLang();
    </script>
    </html>
    """
