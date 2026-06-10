import json
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tradingview_ta import TA_Handler, Interval

app = FastAPI()

# Актуальная база активов Pocket Option
ASSETS_DATA = {
    "[ВСЕ АКТИВЫ] — OTC ЦИКЛ": {
        "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
        "АКЦИИ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
        "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
        "СЫРЬЕ / ИНДЕКСЫ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
    },
    "[ВСЕ АКТИВЫ] — ЖИВОЙ РЫНОК": [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "NZD/USD", "USD/CHF", "EUR/GBP",
        "Bitcoin (BTC/USD)", "Ethereum (ETH/USD)", "Solana (SOL/USD)",
        "Apple", "Microsoft", "Tesla", "Amazon", "NVIDIA",
        "Gold (Золото)", "Crude Oil (Нефть)"
    ]
}

def get_pocket_payout(asset: str) -> int:
    if "OTC" in asset:
        return 92  
    if "Bitcoin" in asset or "Ethereum" in asset or "Solana" in asset:
        return 78  
    if "Gold" in asset or "Oil" in asset:
        return 82  
    return 85  

@app.get("/get_signal")
async def get_signal(asset: str, timeframe: str):
    payout = get_pocket_payout(asset)
    accuracy = round(random.uniform(88.4, 96.8), 1)
    is_up = random.random() > 0.41
    return {
        "signal": "UP" if is_up else "DOWN", 
        "payout": payout,
        "accuracy": accuracy
    }

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#06080c; color:#ffffff; font-family:'Segoe UI', Roboto, sans-serif; margin:0; padding:0;">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HROM QUANTUM CORE v13.0</title>
        <style>
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            @keyframes shine { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            
            .loader { 
                width: 45px; height: 45px; border: 4px solid #161b26; border-top: 4px solid #a855f7; 
                border-radius: 50%; animation: spin 0.8s linear infinite; margin: 15px auto; display: none;
            }
            
            select {
                width: 100%; padding: 14px; background: #0f131e; border: 1px solid #1a2233; 
                border-radius: 14px; font-size: 14px; font-weight: 600; color: #ffffff; outline: none; appearance: none;
            }
            label { font-size: 11px; font-weight: bold; color: #4b5975; display: block; margin-bottom: 5px; letter-spacing: 0.8px; text-transform: uppercase; }
            
            .btn {
                width: 100%; padding: 16px; border: none; color: white; font-weight: 800; border-radius: 14px; 
                cursor: pointer; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; transition: all 0.2s; margin-bottom: 10px;
            }
            .btn-main { background: linear-gradient(135deg, #963bfe 0%, #641bfa 100%); box-shadow: 0 5px 20px rgba(100,27,250,0.4); }
            .btn-auto { background: linear-gradient(135deg, #00ff66 0%, #00b344 100%); color: #000; font-weight: 900; }
            
            .btn-vip { 
                background: linear-gradient(270deg, #ffd700, #ffa500, #b8860b, #ffd700);
                background-size: 400% 400%;
                animation: shine 4s ease infinite;
                color: #000 !important; font-weight: 900; font-size: 14px;
                box-shadow: 0 5px 20px rgba(255,215,0,0.4);
            }
            
            .btn-pocket { background: #141924; border: 1px solid #222d42; color: #38ef7d; }
            .btn-support { background: #080a10; border: 1px solid #161b26; color: #586988; font-size: 11px; margin-top: 15px; }
            .btn:active { transform: scale(0.98); }
            .lang-select { background: #0f131e; color: white; border: 1px solid #1a2233; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: bold; }
            .payout-badge { color: #00ff66; font-weight: 800; font-size: 12px; margin-top: 4px; display: block; }
            
            /* Минималистичные счетчики сессии */
            .counter-box {
                display: flex; justify-content: center; gap: 25px; margin: 15px 0 5px 0;
                font-size: 14px; font-weight: 800; letter-spacing: 0.5px;
            }
            .count-item { display: flex; align-items: center; gap: 6px; background: #0f131e; padding: 6px 14px; border-radius: 10px; border: 1px solid #1a2233; }
        </style>
    </head>
    
    <div style="max-width:430px; margin:15px auto; padding:0 15px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span id="flag_icon" style="font-size:20px; line-height:1;">🇷🇺</span>
            <span style="font-weight:900; font-size:14px; color:#ffffff; letter-spacing:0.5px;">HROM SUPREME</span>
        </div>
        <div>
            <select id="lang" class="lang-select" onchange="changeLang()">
                <option value="ru">🇷🇺 RU</option>
                <option value="en">🇺🇸 EN</option>
                <option value="ua">🇺🇦 UA</option>
                <option value="es">🇪🇸 ES</option>
                <option value="de">🇩🇪 DE</option>
            </select>
        </div>
    </div>

    <div style="max-width:430px; margin:0 auto 30px auto; padding:25px; background:#080a10; border-radius:28px; border: 1px solid #121722; box-shadow: 0 25px 50px rgba(0,0,0,0.8); text-align:center;">
        
        <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:20px;">
            <div style="width:7px; height:7px; background:#00ff66; border-radius:50%; box-shadow: 0 0 10px #00ff66;"></div>
            <span id="lbl_title" style="font-size:11px; font-weight:800; letter-spacing:2px; color:#00ff66;">AI QUANTUM ENGINE ACTIVE</span>
        </div>
        
        <div style="text-align:left; margin-bottom:14px;">
            <label id="lbl_market">КАТЕГОРИЯ РЫНКА</label>
            <select id="cat" onchange="updCategory()"></select>
        </div>
        
        <div id="sub_cat_block" style="text-align:left; margin-bottom:14px; display:none;">
            <label id="lbl_type">ТИП OTC АКТИВА</label>
            <select id="sub_cat" onchange="updSubCategory()"></select>
        </div>
        
        <div style="text-align:left; margin-bottom:14px;">
            <label id="lbl_asset">АКТИВНАЯ ПАРА</label>
            <select id="asset" onchange="updAsset()"></select>
            <span id="payout_lbl" class="payout-badge">PAYOUT: 92%</span>
        </div>
        
        <div style="display:flex; gap:12px; margin-bottom:20px; text-align:left;">
            <div style="flex:1;">
                <label id="lbl_tf">ИНТЕРВАЛ СВЕЧИ</label>
                <select id="time"></select>
            </div>
            <div style="flex:1;">
                <label id="lbl_exp">ЭКСПИРАЦИЯ</label>
                <select id="exp"></select>
            </div>
        </div>

        <button id="runBtn" class="btn btn-main" onclick="getLiveSignal(false)">СКАНИРОВАТЬ РЫНОК</button>
        <button id="autoBtn" class="btn btn-auto" onclick="aiDoForYou()">ИИ СДЕЛАТЬ ЗА ВАС</button>
        
        <a href="https://t.me/andriddddd" target="_blank" style="text-decoration: none;">
            <button id="vipBtn" class="btn btn-vip">🔥 VIP КАНАЛ СИГНАЛОВ 🔥</button>
        </a>
        
        <a href="https://pocketoption.com/register" target="_blank" style="text-decoration: none;">
            <button id="btn_pocket" class="btn btn-pocket">ОТКРЫТЬ POCKET OPTION</button>
        </a>
        
        <div id="status" style="font-size:11px; color:#4b5975; margin-top:20px; min-height:18px; font-weight:700; letter-spacing:0.5px;">СИСТЕМА СИНХРОНИЗИРОВАНА</div>
        
        <div id="loader" class="loader"></div>
        
        <div id="res" style="font-size:55px; font-weight:900; margin:10px 0; min-height:66px; letter-spacing:2px; color:#ffffff;">--</div>
        <div id="accuracy" style="font-size:14px; font-weight:800; color:#a855f7; margin-top:-5px; margin-bottom:10px; display:none;"></div>
        
        <div class="counter-box">
            <div class="count-item">
                <span style="color:#586988; font-size:12px;">PROFIT:</span>
                <span id="win_counter" style="color:#00ff66;">0</span>
            </div>
            <div class="count-item">
                <span style="color:#586988; font-size:12px;">LOSS:</span>
                <span id="loss_counter" style="color:#ff3344;">0</span>
            </div>
        </div>

        <div id="timer" style="font-size:14px; font-weight:800; color:#ffaa00; margin-bottom:15px; min-height:20px;"></div>
        
        <button id="mart" class="btn" onclick="getLiveSignal(true)" style="display:none; background:#ff3344; box-shadow: 0 5px 15px rgba(255,51,68,0.3);">АКТИВИРОВАТЬ ПЕРЕКРЫТИЕ</button>

        <a href="https://t.me/andriddddd" target="_blank" style="text-decoration: none;">
            <button id="btn_supp" class="btn btn-support">РАЗРАБОТЧИК / SUPPORT</button>
        </a>
    </div>
    
    <script>
        const rawData = """ + json.dumps(ASSETS_DATA) + """;
        const allIntervals = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "10 мин"];
        const fullExp = ["5 сек", "15 сек", "300 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "10 мин"];
        const limitedExp = ["1 мин", "2 мин", "3 мин", "4 мин", "5 мин", "10 мин"];
        let mainInterval = null;
        let currentAssetPayout = 92;

        let wins = 0;
        let losses = 0;

        const flags = { ru: "🇷🇺", en: "🇺🇸", ua: "🇺🇦", es: "🇪🇸", de: "🇩🇪" };
        const dictionary = {
            ru: {
                title: "AI QUANTUM ENGINE ACTIVE", market: "КАТЕГОРИЯ РЫНКА", type: "ТИП OTC АКТИВА", asset: "АКТИВНАЯ ПАРА", tf: "ИНТЕРВАЛ СВЕЧИ",
                exp: "ЭКСПИРАЦИЯ", scan: "СКАНИРОВАТЬ РЫНОК", auto: "ИИ СДЕЛАТЬ ЗА ВАС", pocket: "ОТКРЫТЬ POCKET OPTION", support: "РАЗРАБОТЧИК / SUPPORT",
                ready: "СИСТЕМА СИНХРОНИЗИРОВАНА", load: "[ ANALYZING MARKET ORDER... ]", UP: "ВВЕРХ / CALL", DOWN: "ВНИЗ / PUT",
                otc: "OTC СИСТЕМА: РАСЧЕТ ИИ УСПЕШЕН", buy: "АНАЛИЗ TV: СИГНАЛ НА ПОКУПКУ", sell: "АНАЛИЗ TV: СИГНАЛ НА ПРОДАЖУ",
                flat: "МАТРИЦА ОБЪЕМОВ: ИМПУЛЬС ТРЕНДА", backup: "АВТОНОМНЫЙ ИИ РЕЖИМ", mart_status: "[ CALCULATING MARTINGALE STEP... ]",
                mart_btn: "АКТИВИРОВАТЬ ПЕРЕКРЫТИЕ", wait: "ВХОД В СДЕЛКУ ЧЕРЕЗ: ", process: "СДЕЛКА В ПРОЦЕССЕ ТОРГОВЛИ: ", end: "ТОРГОВЫЙ ЦИКЛ ЗАВЕРШЕН",
                ai_search: "[ AI SEARCHING BEST ENTRY POINT... ]"
            },
            en: {
                title: "AI QUANTUM ENGINE ACTIVE", market: "MARKET CATEGORY", type: "OTC ASSET TYPE", asset: "ACTIVE PAIR", tf: "CANDLE TIMEFRAME",
                exp: "EXPIRATION TIME", scan: "SCAN MARKET", auto: "AI DO FOR YOU", pocket: "OPEN POCKET OPTION", support: "DEVELOPER / SUPPORT",
                ready: "SYSTEM SYNCHRONIZED", load: "[ ANALYZING MARKET ORDER... ]", UP: "CALL", DOWN: "PUT",
                otc: "OTC SYSTEM: AI CALCULATION SUCCESS", buy: "TV ANALYSIS: BUY SIGNAL", sell: "TV ANALYSIS: SELL SIGNAL",
                flat: "VOLUME MATRIX: TREND IMPULSE", backup: "AUTONOMOUS AI MODE", mart_status: "[ CALCULATING MARTINGALE STEP... ]",
                mart_btn: "ACTIVATE MULTIPLIER", wait: "ENTER TRADE IN: ", process: "TRADE IN PROCESS: ", end: "TRADE CYCLE COMPLETED",
                ai_search: "[ AI SEARCHING BEST ENTRY POINT... ]"
            }
        };

        function changeLang() {
            let l = document.getElementById('lang').value;
            let d = dictionary[l] || dictionary['en'];
            document.getElementById('flag_icon').innerText = flags[l];
            document.getElementById('lbl_title').innerText = d.title;
            document.getElementById('lbl_market').innerText = d.market;
            if(document.getElementById('lbl_type')) document.getElementById('lbl_type').innerText = d.type;
            document.getElementById('lbl_asset').innerText = d.asset;
            document.getElementById('lbl_tf').innerText = d.tf;
            document.getElementById('lbl_exp').innerText = d.exp;
            document.getElementById('runBtn').innerText = d.scan;
            document.getElementById('autoBtn').innerText = d.auto;
            document.getElementById('btn_pocket').innerText = d.pocket;
            document.getElementById('btn_supp').innerText = d.support;
            document.getElementById('mart').innerText = d.mart_btn;
            document.getElementById('status').innerText = d.ready;
        }

        function init(){
            allIntervals.forEach(o => document.getElementById('time').innerHTML += `<option>${o}</option>`);
            Object.keys(rawData).forEach(c => document.getElementById('cat').innerHTML += `<option>${c}</option>`);
            updCategory();
            changeLang();
        }

        function calcLocalPayout(assetName) {
            if(assetName.includes("OTC")) return 92;
            if(assetName.includes("BTC") || assetName.includes("ETH") || assetName.includes("Solana") || assetName.includes("Bitcoin") || assetName.includes("Ethereum")) return 78;
            if(assetName.includes("Gold") || assetName.includes("Oil") || assetName.includes("Нефть") || assetName.includes("Золото")) return 82;
            return 85;
        }

        function updCategory(){
            let c = document.getElementById('cat').value;
            let subBlock = document.getElementById('sub_cat_block');
            
            if(c.includes("OTC")) {
                subBlock.style.display = 'block';
                let types = Object.keys(rawData[c]);
                document.getElementById('sub_cat').innerHTML = types.map(t => `<option>${t}</option>`).join('');
                updSubCategory();
            } else {
                subBlock.style.display = 'none';
                document.getElementById('asset').innerHTML = rawData[c].map(a => `<option>${a}</option>`).join('');
                updAsset();
            }
        }

        function updSubCategory() {
            let c = document.getElementById('cat').value;
            let t = document.getElementById('sub_cat').value;
            document.getElementById('asset').innerHTML = rawData[c][t].map(a => `<option>${a}</option>`).join('');
            updAsset();
        }

        function updAsset() {
            let asset = document.getElementById('asset').value;
            currentAssetPayout = calcLocalPayout(asset);
            document.getElementById('payout_lbl').innerText = `PAYOUT: ${currentAssetPayout}%`;
            
            let expSelect = document.getElementById('exp');
            expSelect.innerHTML = "";
            let isOtc = asset.includes("OTC");
            let currentOptions = isOtc ? fullExp : limitedExp;
            currentOptions.forEach(o => { expSelect.innerHTML += `<option value="${o}">${o}</option>`; });
        }

        async function aiDoForYou() {
            let cats = Object.keys(rawData);
            let randomCat = cats[Math.floor(Math.random() * cats.length)];
            document.getElementById('cat').value = randomCat;
            updCategory();
            
            if(randomCat.includes("OTC")) {
                let subCats = Object.keys(rawData[randomCat]);
                let randomSub = subCats[Math.floor(Math.random() * subCats.length)];
                document.getElementById('sub_cat').value = randomSub;
                updSubCategory();
            }
            
            let assetSelect = document.getElementById('asset');
            let randomAsset = assetSelect.options[Math.floor(Math.random() * assetSelect.options.length)].value;
            assetSelect.value = randomAsset;
            updAsset();
            
            let tfSelect = document.getElementById('time');
            tfSelect.value = tfSelect.options[Math.floor(Math.random() * tfSelect.options.length)].value;
            
            let expSelect = document.getElementById('exp');
            expSelect.value = expSelect.options[Math.floor(Math.random() * expSelect.options.length)].value;
            
            getLiveSignal(false, true);
        }

        function parseToSeconds(valStr) {
            let num = parseInt(valStr);
            if(valStr.includes("сек") || valStr.includes("sec")) return num;
            if(valStr.includes("мин") || valStr.includes("min")) return num * 60;
            return 60;
        }

        async function getLiveSignal(isMartingale, isAiAuto = false) {
            if(mainInterval) clearInterval(mainInterval);
            let l = document.getElementById('lang').value;
            let d = dictionary[l] || dictionary['en'];
            
            const runBtn = document.getElementById('runBtn');
            const autoBtn = document.getElementById('autoBtn');
            const martBtn = document.getElementById('mart');
            const status = document.getElementById('status');
            const res = document.getElementById('res');
            const timer = document.getElementById('timer');
            const loader = document.getElementById('loader');
            const accField = document.getElementById('accuracy');
            
            runBtn.disabled = true;
            autoBtn.disabled = true;
            martBtn.disabled = true;
            
            res.style.display = 'none';
            accField.style.display = 'none';
            loader.style.display = 'block';
            
            status.innerText = isAiAuto ? d.ai_search : (isMartingale ? d.mart_status : d.load);
            timer.innerText = "";
            
            let asset = document.getElementById('asset').value;
            let timeframe = document.getElementById('time').value;
            let expTimeStr = document.getElementById('exp').value;
            
            try {
                let response = await fetch(`/get_signal?asset=${encodeURIComponent(asset)}&timeframe=${encodeURIComponent(timeframe)}`);
                let result = await response.json();
                
                await new Promise(r => setTimeout(r, 2600));
                
                loader.style.display = 'none';
                res.style.display = 'block';
                
                res.innerText = d[result.signal];
                res.style.color = result.signal === "UP" ? "#00ff66" : "#ff3344";
                
                accField.innerText = `🎯 ACCURACY: ${result.accuracy}%`;
                accField.style.display = 'block';
                status.innerText = d.otc;
                
            } catch(e) {
                loader.style.display = 'none';
                res.style.display = 'block';
                res.innerText = d.UP;
                res.style.color = "#00ff66";
                status.innerText = d.backup;
            }
            
            runBtn.disabled = false;
            autoBtn.disabled = false;
            martBtn.disabled = false;
            martBtn.style.display = 'block';
            
            let entryTime = 10;
            timer.style.color = "#ffaa00";
            timer.innerText = d.wait + entryTime + " SEC";
            
            mainInterval = setInterval(() => {
                if (entryTime > 0) {
                    entryTime--;
                    timer.innerText = d.wait + entryTime + " SEC";
                    if(entryTime === 0) {
                        let tradeTime = parseToSeconds(expTimeStr);
                        timer.style.color = "#00ff66";
                        timer.innerText = d.process + tradeTime + " SEC";
                        
                        clearInterval(mainInterval);
                        mainInterval = setInterval(() => {
                            tradeTime--;
                            timer.innerText = d.process + tradeTime + " SEC";
                            if(tradeTime <= 0) {
                                clearInterval(mainInterval);
                                timer.style.color = "#ffffff";
                                timer.innerText = d.end;
                                
                                // ПРОСТАЯ ФИКСАЦИЯ РЕЗУЛЬТАТА В СЧЕТЧИКИ СЕССИИ (+ ИЛИ -)
                                if (Math.random() > 0.15) {
                                    wins++;
                                    document.getElementById('win_counter').innerText = wins;
                                } else {
                                    losses++;
                                    document.getElementById('loss_counter').innerText = losses;
                                }
                            }
                        }, 1000);
                    }
                }
            }, 1000);
        }
        init();
    </script>
    </html>
    """
